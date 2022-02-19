import networkx as nx
from securitygames.environment import Network
from securitygames.attacker import Attacker
from securitygames.defender import ObliviousDefender

GAME_LENGTH = 10

if __name__ == "__main__":
    net = Network()
    attacker = Attacker()
    defender = ObliviousDefender()
    for t in range(GAME_LENGTH):
        attacker_done = False
        defender_done = False
        while not attacker_done:
            attacker.act(net)
        while not defender_done:
            defender.act(net)
        pwnd_nodes = net.list_pwnd_nodes()
        print(f"{len(pwnd_nodes)} Nodes pwnd at end of round {t}:\n {pwnd_nodes}\n")