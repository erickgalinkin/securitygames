import random

class Defender:
    def __init__(self):
        self.alerts = list()

    def act(self, net):
        new_alerts = self._check_alerts(net)
        if new_alerts:
            print("You have new alerts to review.")
        input_string = f""" Choose your action:
        [1] View alerts
        [2] View node status
        [3] Hunt in logs
        [4] Configure firewall
        [5] Isolate node
        [6] Remediate node
        [7] No action\n
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
            for alert in self.alerts:
                print(alert)
            return False
        elif action == 2:
            node_to_inspect = input("Input a node name to inspect.\t")
            return self._inspect_node(net, node_to_inspect.lower())
        elif action == 3:
            log_info = self._hunt_logs(net)
            if len(log_info) > 0:
                print(f"Suspicious log entries found!\n{log_info}")
            else:
                print("Nothing significant to report.\n")
            return True
        elif action == 4:
            node_to_firewall = input("Input a node to firewall.\t")
            if node_to_firewall not in net.nodes:
                print("Please select a valid node.")
                return False
            firewall_applied = self._apply_firewall(net, node_to_firewall)
            if not firewall_applied:
                print("Firewall not applied. The node is not internet-facing.")
            return firewall_applied
        elif action == 5:
            node_to_isolate = input("Input a node to isolate.\t")
            if node_to_isolate not in net.nodes:
                print("Please select a valid node.")
                return False
            self._perform_isolation(net, node_to_isolate)
            return True
        elif action == 6:
            node_to_remediate = input("Input a node to remediate.\t")
            remediated = self._remediate_node(net, node_to_remediate)
            if remediated:
                print(f"{node_to_remediate} remediated!")
            return remediated
        elif action == 7:
            return self._do_nothing()
        else:
            print("Action not recognized.")
            return False

    def _check_alerts(self, net):
        alert_list = list()
        for i in net.nodes:
            logs = net.nodes[i]["data"].inspect_asset()
            if not logs:
                continue
            for item in logs:
                item_components = item.split(",")
                if item_components[0] == "ALERT":
                    alert_list.append(item)
        new_alerts = True if alert_list != self.alerts else False
        self.alerts = alert_list
        return new_alerts

    @staticmethod
    def _inspect_node(net, node_to_inspect):
        if node_to_inspect not in net.nodes:
            print("Not a valid node")
            return False
        ransomwared = str(net.nodes[node_to_inspect]["data"].is_ransomwared)
        pwnd = str(net.nodes[node_to_inspect]["data"].is_pwnd)
        internet = str(net.nodes[node_to_inspect]["data"].is_internet_facing)
        print(f"Node name: {node_to_inspect}\nInternet facing: {internet}\nPwnd: {pwnd}\nRansomwared: {ransomwared}\n")
        return False

    def _hunt_logs(self, net):
        suspicious_logs = list()
        nodes_of_interest = set()
        if self.alerts:
            for alert in self.alerts:
                node_of_interest, _ = self._parse_alert(alert)
                nodes_of_interest.add(node_of_interest)
        for i in net.nodes:
            logs = net.nodes[i]["data"].inspect_asset()
            if not logs:
                continue
            if i in nodes_of_interest:
                suspicious_logs.extend(logs)
                continue
            else:
                for item in logs:
                    p_hunt = random.random()
                    if p_hunt > 0.65:
                        suspicious_logs.append(item)
        return suspicious_logs

    @staticmethod
    def _do_nothing(*args):
        print("Defender took no action.")
        return True

    @staticmethod
    def _perform_isolation(net, node):
        node_edges = list(net.edges([node]))
        edge_count = len(node_edges)
        net.nodes[node]["data"].quarantine()
        net.remove_edges_from(node_edges)
        net.connectivity -= edge_count
        print("Connectivity is reduced!")

    @staticmethod
    def _parse_alert(alert):
        alert_components = alert.split(",")
        affected_node = alert_components[2]
        alert_msg = alert_components[1]
        return affected_node, alert_msg

    @staticmethod
    def _remediate_node(net, node):
        return net.nodes[node]["data"].remediate_asset()

    @staticmethod
    def _apply_firewall(net, node):
        firewall_applied = net.apply_firewall(node)
        return firewall_applied


class ObliviousDefender(Defender):
    def __init__(self):
        super(ObliviousDefender, self).__init__()
        pass

    def act(self, net):
        return self._do_nothing()


# Default class for simulation
class PassiveDefender(Defender):
    def __init__(self):
        super(PassiveDefender, self).__init__()

    def act(self, net):
        new_alerts = self._check_alerts(net)
        if not new_alerts:
            return True
        active_alert = self.alerts[0]
        affected_node, alert_msg = self._parse_alert(active_alert)
        action = self.next_best_action(net, affected_node, alert_msg)
        return action

    def next_best_action(self, net, affected_node, alert_msg):
        action_map = {"RANSOMWARE_DETECTED_SUCCESS=TRUE": self._remediate_node,
                      "RANSOMWARE_DETECTED_SUCCESS=FALSE": self._apply_firewall,
                      "privesc_succcess": self._remediate_node,
                      "privesc_failure": self._remediate_node,
                      "psexec_attempt": self._do_nothing
                      }
        action = action_map.get(alert_msg, self._do_nothing)
        result = action(net, affected_node)
        return True