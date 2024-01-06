import common
from colorama import Fore, Back, Style


def simple_dfs_fight(b_hp, b_dmg, p_hp=50, p_mana=500):
    return min(dfs(b_hp, b_dmg, p_hp, p_mana, 0, 0, 0, 0, 0))


def hard_dfs_fight(b_hp, b_dmg, p_hp=50, p_mana=500):
    return min(dfs(b_hp, b_dmg, p_hp, p_mana, 0, 0, 0, 0, 1))


def dfs(b_hp, b_dmg, p_hp, p_mana, spent_mana, shield, poison, recharge, penalty):
    p_hp -= penalty
    if p_hp <= 0:
        return # dead, do not yield

    # apply effects
    if poison > 0:
        b_hp -= 3
    if recharge > 0:
        p_mana += 101
    shield = max(0, shield - 1)
    poison = max(0, poison - 1)
    recharge = max(0, recharge - 1)

    # check if boss is dead
    if b_hp <= 0:
        yield spent_mana
    elif b_hp <= 7 and poison > 0 and p_mana >= 53:
        # boss will die of poison next turn, helped by missile
        # special handling due to "death on boss turn"
        yield spent_mana + 53
    else:
        # cast each spell you can afford and "split" itself
        # then run boss turn and return all results
        if p_mana >= 53:
            yield from dfs(b_hp - 4 - (3 if poison > 0 else 0),
                           b_dmg,
                           p_hp - (b_dmg - 7 if shield > 0 else b_dmg),
                           p_mana - 53 + (101 if recharge > 0 else 0),
                           spent_mana + 53,
                           max(0, shield - 1),
                           max(0, poison - 1),
                           max(0, recharge - 1),
                           penalty)
        if p_mana >= 73:
            yield from dfs(b_hp - 2 - (3 if poison > 0 else 0),
                           b_dmg,
                           p_hp + 2 - (b_dmg - 7 if shield > 0 else b_dmg),
                           p_mana - 73 + (101 if recharge > 0 else 0),
                           spent_mana + 73,
                           max(0, shield - 1),
                           max(0, poison - 1),
                           max(0, recharge - 1),
                           penalty)
        if p_mana >= 113 and shield == 0:
            yield from dfs(b_hp - (3 if poison > 0 else 0),
                           b_dmg,
                           p_hp - (b_dmg - 7),
                           p_mana - 113 + (101 if recharge > 0 else 0),
                           spent_mana + 113,
                           5,
                           max(0, poison - 1),
                           max(0, recharge - 1),
                           penalty)
        if p_mana >= 173 and poison == 0:
            yield from dfs(b_hp - 3,
                           b_dmg,
                           p_hp - (b_dmg - 7 if shield > 0 else b_dmg),
                           p_mana - 173 + (101 if recharge > 0 else 0),
                           spent_mana + 173,
                           max(0, shield - 1),
                           5,
                           max(0, recharge - 1),
                           penalty)
        if p_mana >= 229 and recharge == 0:
            yield from dfs(b_hp - (3 if poison > 0 else 0),
                           b_dmg,
                           p_hp - (b_dmg - 7 if shield > 0 else b_dmg),
                           p_mana - 229 + 101,
                           spent_mana + 229,
                           max(0, shield - 1),
                           max(0, poison - 1),
                           4,
                           penalty)


assert simple_dfs_fight(13, 8, 10, 250) == 226
assert simple_dfs_fight(14, 8, 10, 250) == 641

b_hp, b_dmg = [int(x.split(': ')[1]) for x in common.Loader.load_lines()]
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{simple_dfs_fight(b_hp, b_dmg)}')

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{hard_dfs_fight(b_hp, b_dmg)}')