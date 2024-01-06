import math

import common
from colorama import Fore, Back, Style

WEAPONS = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
ARMORS = [(0, 0, 0), (13, 0 ,1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
RINGS = [(0, 0, 0), (0, 0, 0), (25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]

# take boss HP / player damage - boss armor
# vice versa and compare "time to beat"
def combat(p_hp, p_attack, p_def, b_hp, b_attack, b_def):
    p_damage = max(1, p_attack - b_def)
    b_damage = max(1, b_attack - p_def)
    p_turns = math.ceil(b_hp / p_damage)
    b_turns = math.ceil(p_hp / b_damage)
    return p_turns <= b_turns

def find_equip(win=True):
    b_hp, b_attack, b_def = [int(x.split(': ')[1]) for x in common.Loader.load_lines()]
    p_hp = 100

    result = []

    # for each combo evaluate price, attack and defense and save those that "win"
    for w in WEAPONS:
        for a in ARMORS:
            for i in range(len(RINGS)):
                for i2 in range(i + 1, len(RINGS)):
                    price = w[0] + a[0] + RINGS[i][0] + RINGS[i2][0]
                    attack = w[1] + a[1] + RINGS[i][1] + RINGS[i2][1]
                    defense = w[2] + a[2] + RINGS[i][2] + RINGS[i2][2]
                    result.append((price, attack, defense, combat(p_hp, attack, defense, b_hp, b_attack, b_def)))

    # sort by price
    valid = sorted([r for r in result if r[3]], key=lambda x: x[0])
    invalid = sorted([r for r in result if not r[3]], key=lambda x: x[0])
    return valid[0][0] if win else invalid[-1][0]


assert combat(8, 5, 5, 12, 7, 2)
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{find_equip()}')
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{find_equip(False)}')


# 282 is TOO HIGH?