from securitygames.environment import Network
from securitygames.attacker import Attacker
from securitygames.defender import Defender

GAME_LENGTH = 15
RANSOM_VALUE = 5
TARGET_RANSOM_VALUE = 25
TARGET_PWND_VALUE = 10


def attacker_wins(net):
    # TODO: Improve attacker win condition
    if net.ransomed:
        for node in net.targets:
            if net.nodes[node]["data"].ransomed:
                return True
    return False


def score_game(net):
    attacker_score = 0
    defender_score = 0
    defender_score += net.connectivity
    for node in net:
        if net.nodes[node]["data"].is_target:
            if net.nodes[node]["data"].is_pwnd:
                attacker_score += TARGET_PWND_VALUE
            else:
                defender_score += TARGET_PWND_VALUE
            if net.nodes[node]["data"].ransomed:
                attacker_score += TARGET_RANSOM_VALUE
            else:
                defender_score += TARGET_RANSOM_VALUE
        else:
            if net.nodes[node]["data"].is_pwnd:
                attacker_score += 1
            else:
                defender_score += 1
            if net.nodes[node]["data"].ransomed:
                attacker_score += RANSOM_VALUE
            else:
                defender_score += RANSOM_VALUE
    return attacker_score, defender_score


if __name__ == "__main__":
    net = Network()
    attacker = Attacker()
    defender = Defender()
    for t in range(GAME_LENGTH):
        attacker_done = False
        defender_done = False
        while not attacker_done:
            attacker_done = attacker.act(net)
        while not defender_done:
            defender_done = defender.act(net)
        if attacker_wins(net):
            break
        pwnd_nodes = net.list_pwnd_nodes()
        # TODO: This print statement leaks info to the defender.
        # print(f"{len(pwnd_nodes)} Nodes pwnd at end of round {t+1}:\n {pwnd_nodes}\n")
    attacker_score, defender_score = score_game(net)
    max_score = attacker_score + defender_score
    print(f"Attacker score: {attacker_score}\n"
          f"Defender score: {defender_score}\n"
          f"Max score: {max_score}")
    if attacker_score > defender_score:
        print("Attacker wins!")
    if defender_score > attacker_score:
        print("Defender wins!")
    print("See ya next time!")
