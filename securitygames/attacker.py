import networkx as nx


class Attacker:
    def __init__(self):
        self.location = "internet"
        self.credentials = list()
        self.exploits = list()
        self.malware = list()
        self.accessible_nodes = list()
        self.is_admin = False

    def act(self, net):
        input_string = f""" You are currently at location: {self.location}
        Choose your action:
        [1] Show accessible nodes
        [2] Scan for accessible nodes
        [3] Inspect a node
        [4] Exploit a node
        [5] Move laterally to a node
        [6] Escalate privileges
        [7] Install ransomware
        [8] Execute ransomware\n
        """
        action = input(input_string).strip()
        if action == "q" or action == "quit" or action == "exit":
            confirmation = input("Are you sure you want to quit? [Y]/n\t")
            if confirmation.lower() != "n" and confirmation.lower() != "no":
                print("See ya next time!")
                exit()
        try:
            action = int(action)
        except ValueError:
            print("Please enter only integer values.")
            return False
        if action == 1:
            if len(self.accessible_nodes) < 1:
                print("No accessible nodes")
            else:
                print(self.accessible_nodes)
            return False
        elif action == 2:
            self.accessible_nodes = self._scan_network(net)
            print(self.accessible_nodes)
            return True
        elif action == 3:
            node_to_inspect = input("Input a node name to inspect or type \"current\" to inspect your current location.\t")
            return self._inspect_node(net, node_to_inspect.lower())
        elif action == 4:
            node_to_exploit = input("Input a node name to exploit.\t")
            return self._exploit_node(net, node_to_exploit)
        elif action == 5:
            if len(self.accessible_nodes) == 0:
                print("No nodes to move to.")
                return False
            else:
                node_to_move = input("Input a node to move to.\t")
                if node_to_move not in self.accessible_nodes:
                    print("That node is not accessible.")
                    return False
                else:
                    lateral_movement = net.nodes[node_to_move]["data"].lateral_movement(self.is_admin)
                    if lateral_movement:
                        self.location = node_to_move
                    return lateral_movement
        elif action == 6:
            return True
        elif action == 7:
            return True
        elif action == 8:
            return True
        else:
            print("Action not recognized")
            return False

    def _scan_network(self, net):
        accessible_nodes = list()
        if self.location == "internet":
            for i in net.nodes:
                if net.nodes[i]["data"].is_internet_facing:
                    accessible_nodes.append(net.nodes[i]["data"].name)
            return accessible_nodes
        else:
            return accessible_nodes

    def _inspect_node(self, net, node_to_inspect):
        print(node_to_inspect)
        if node_to_inspect == "current":
            node_to_inspect = self.location
            if node_to_inspect == "internet":
                print("Nothing to inspect")
                return False
        ransomwared = str(net.nodes[node_to_inspect]["data"].ransomwared)
        pwnd = str(net.nodes[node_to_inspect]["data"].is_pwnd)
        target = str(net.nodes[node_to_inspect]["data"].is_target) if node_to_inspect in self.accessible_nodes \
            else "Unknown"
        print(f"Node name: {node_to_inspect}\nPwnd: {pwnd}\nRansomwared: {ransomwared}\nIs target: {target}\n")
        return False

    def _exploit_node(self, net, node_to_exploit):
        return True
