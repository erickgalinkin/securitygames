import networkx as nx
import random
import numpy as np


class Account:
    def __init__(self, username, admin=False, difficulty=0):
        self.name = username
        self.admin = admin
        self.password = self.generate_password(difficulty)
        self.pw_difficulty = difficulty

    @staticmethod
    def generate_password(difficulty: int) -> int:
        password = random.randint(0, 2 ** difficulty)
        return password

    def change_password(self):
        self.password = self.generate_password(self.pw_difficulty)


class Asset:
    def __init__(self):
        self.name = "asset_" + str(random.randint(0, 100))
        self.is_pwnd = False
        self.ransomwared = False
        self.is_target = False
        self.is_internet_facing = False
        self.log = list()

    def inspect_asset(self):
        return self.log

    def detect_scanning(self, location):
        if random.random() > 0.5:
            self.log.append(f"INFO,scanning_from_{location},{self.name}")

    def exploit_asset(self):
        if self.is_pwnd:
            print("Asset already pwnd!")
            return True
        p_success = random.random()
        p_detection = random.random()
        p_attempt = random.random()
        if p_attempt > p_success:
            self.is_pwnd = True
            if p_detection > 0.5:
                self.log.append(f"ALERT,exploitation_succcess,{self.name}")
            return True
        else:
            if p_detection > p_attempt:
                self.log.append(f"ALERT,exploitation_failure,{self.name}")
            return False

    def lateral_movement(self, is_admin=False):
        if self.is_pwnd or is_admin:
            print("Lateral Movement Succeeded.")
            self.is_pwnd = True
            return True
        elif not is_admin:
            print("Lateral Movement Failed. No valid credentials.")
            return False
        else:
            print("Lateral Movement Failed. Machine not pwnd")
            return False

    def privilege_escalation(self):
        p_success = random.random()
        p_detection = random.random()
        p_attempt = random.random()
        if p_attempt > p_success:
            print("Privilege escalation succeeded!")
            if p_detection > 0.25:
                self.log.append(f"ALERT,privesc_succcess,{self.name}")
            return True
        else:
            print("Privilege escalation failed.")
            if p_detection > 0.1:
                self.log.append(f"ALERT,privesc_failure,{self.name}")
            return False

    def remediate_asset(self):
        if self.is_pwnd:
            self.is_pwnd = False
            self.ransomwared = False
            return True

    def configure_asset_firewall(self):
        self.is_internet_facing = False
        return True


class Server(Asset):
    def __init__(self):
        self.name = "server_" + str(random.randint(0, 100))
        self.processes = self.define_server()

    @staticmethod
    def define_server():
        # example = {80: {
        #     "procname": "Apache",
        #     "vulnerable": False
        # }}
        # TODO: autogenerate processes
        processes = dict()
        return processes

    def exploit_service(self, port):
        if port not in self.processes.keys():
            self.log.append(f"INFO,dropped_packet,port:{port}")
        else:
            process = self.processes[port]


class Workstation(Asset):
    def __init__(self):
        self.name = "workstation_" + str(random.randint(0,100))
        self.smb = True
        self.processes = list()

    def connect_psexec(self, creds):
        if not creds.admin:
            self.log.append(f"ALERT,psexec_attempt,{creds.name}")
        else:
            self.is_pwnd = True


class Network(nx.Graph):
    def __init__(self, size=5):
        super(Network, self).__init__()
        self.asset_list = list()
        self._update_asset_list()
        self._generate_random_network(size)

    def _generate_random_network(self, size):
        target = Asset()
        target.is_target = True
        target.is_internet_facing = True if random.random() > 0.9 else False
        self.add_node(target.name, data=target)

        for i in range(size - 1):
            node = Asset()
            node.is_internet_facing = True if random.random() > 0.5 else False
            self.add_node(node.name, data=node)
            self._update_asset_list()
            nodearray = np.array(self.asset_list)
            for k in range(i):
                p_add_edge = random.random()
                if p_add_edge > 0:
                    node1 = nodearray[random.randint(k, i)]
                    node2 = nodearray[random.randint(k, i)]
                    if node1 != node2 and not self.has_edge(node1, node2):
                        self.add_edge(node1, node2)

    def _update_asset_list(self):
        self.asset_list = list(self.nodes())

    def list_pwnd_nodes(self):
        pwnd_nodes = list()
        for node in self.nodes:
            if self.nodes[node]["data"].is_pwnd:
                pwnd_nodes.append(node)

        return pwnd_nodes
