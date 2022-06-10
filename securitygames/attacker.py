class Attacker:
    """
    Base attacker class
    """
    def __init__(self):
        # TODO: Use of credentials, exploits, malware
        self.location = "internet"
        self.credentials = list()
        self.exploits = list()
        self.malware = list()
        self.accessible_nodes = list()
        self.is_admin = False

    def act(self, net):
        if self.location in net.nodes:
            if net.nodes[self.location]["data"].isolated:
                print("You were on a node that was isolated from the network and have been disconnected.")
                self.accessible_nodes.remove(self.location)
                self.location = "internet"
        input_string = f""" You are currently at location: {self.location}
        Choose your action:
        [1] Show accessible nodes
        [2] Scan for accessible nodes
        [3] Inspect a node
        [4] Exploitation attempt
        [5] Lateral movement attempt
        [6] Privilege escalation attempt
        [7] Install ransomware on current node attempt
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
            self._scan_network(net)
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
            if self.is_admin:
                print("Already administrator!")
                return False
            if self.location not in net.nodes:
                print("Cannot escalate privileges from outside the network. Move to a valid asset.")
                return False
            else:
                privesc_success = self._privesc(net)
                self.is_admin = privesc_success
            return True
        elif action == 7:
            if self.location not in net.nodes:
                print("Cannot install ransomware from outside the network!")
                return False
            if net.nodes[self.location]["data"].is_ransomwared:
                print("Already installed ransomware!")
            net.nodes[self.location]["data"].install_malware("ransomware", self.is_admin)
            return True
        elif action == 8:
            self._execute_ransomware(net)
            return True
        else:
            print("Action not recognized")
            return False

    def _scan_network(self, net):
        if self.location == "internet":
            accessible_nodes = list()
            for i in net.nodes:
                if net.nodes[i]["data"].is_internet_facing:
                    accessible_nodes.append(net.nodes[i]["data"].name)
        else:
            accessible_nodes = [n for n in net.neighbors(self.location)]
        net.detect_scanning(self.location)
        self.accessible_nodes += accessible_nodes
        self.accessible_nodes = list(set(self.accessible_nodes))
        return True

    def _inspect_node(self, net, node_to_inspect):
        if node_to_inspect == "current":
            node_to_inspect = self.location
            if node_to_inspect == "internet":
                print("Nothing to inspect")
                return False
        if node_to_inspect not in self.accessible_nodes:
            print("Not a valid node")
            return False
        ransomwared = str(net.nodes[node_to_inspect]["data"].is_ransomwared)
        pwnd = str(net.nodes[node_to_inspect]["data"].is_pwnd)
        target = str(net.nodes[node_to_inspect]["data"].is_target) if node_to_inspect in self.accessible_nodes \
            else "Unknown"
        print(f"Node name: {node_to_inspect}\nPwnd: {pwnd}\nRansomwared: {ransomwared}\nIs target: {target}\n")
        return False

    def _exploit_node(self, net, node_to_exploit):
        if net.nodes[node_to_exploit]["data"].is_pwnd:
            print("Asset already pwnd!")
            return False
        if node_to_exploit not in self.accessible_nodes:
            print("That node is not accessible!")
            return False
        # TODO: modify exploit_asset to use exploits from attacker exploit list
        exploit_success = net.nodes[node_to_exploit]["data"].exploit_asset()
        if exploit_success:
            print(f"{node_to_exploit} pwnd!")
            if self.location == "internet":
                self.location = node_to_exploit
        else:
            print(f"{node_to_exploit} not pwnd. :(")
        return True

    def _privesc(self, net):
        return net.nodes[self.location]["data"].privilege_escalation()

    def _execute_ransomware(self, net):
        for node in self.accessible_nodes:
            net.nodes[node]["data"].ransom_asset()
        net.ransom_executed()


class DefaultAttacker(Attacker):
    def __init__(self):
        super(DefaultAttacker, self).__init__()
        self.scanned_from = list()

    def act(self, net):
        if self.location == "internet" and len(self.accessible_nodes) == 0:
            return self._scan_network(net)
        elif len(self.accessible_nodes - self.scanned_from) == 0:
            return self._scan_network(net)
        elif self.location == "internet" and len(self.accessible_nodes) > 0:
            node = self.choose_best_node()
            self._exploit_node(net, self.accessible_nodes[0])
        elif

    def _inspect_node(self, net, node_to_inspect):
        if node_to_inspect == "current":
            node_to_inspect = self.location
            if node_to_inspect == "internet":
                print("Nothing to inspect")
                return False
        if node_to_inspect not in self.accessible_nodes:
            print("Not a valid node")
            return False
        ransomwared = str(net.nodes[node_to_inspect]["data"].is_ransomwared)
        pwnd = str(net.nodes[node_to_inspect]["data"].is_pwnd)
        target = str(net.nodes[node_to_inspect]["data"].is_target) if node_to_inspect in self.accessible_nodes \
            else "Unknown"
        return ransomwared, pwnd, target