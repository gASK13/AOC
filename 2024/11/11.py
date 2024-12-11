import common
from colorama import Fore, Back

_CACHE = {}

def blink_stone(stone, count):
    if (stone, count) in _CACHE:
        return _CACHE[(stone, count)]

    if count == 0:
        return 1

    if stone == 0:
        rv = blink_stone(1, count - 1)
    elif len(str(stone)) % 2 == 0:
        stone_text = str(stone)
        half = len(stone_text) // 2
        rv = blink_stone(int(stone_text[:half]), count-1) + blink_stone(int(stone_text[half:]), count-1)
    else:
        rv = blink_stone(stone * 2024, count-1)
    _CACHE[(stone, count)] = rv
    return rv


def blink(stones, count):
    return sum([blink_stone(s, count) for s in stones])


assert blink([0,1,10,99,999], 1) == 7
assert blink([125,17], 1) == 3
assert blink([125,17], 2) == 4
assert blink([125,17], 3) == 5
assert blink([125,17], 4) == 9
assert blink([125,17], 5) == 13
assert blink([125,17], 6) == 22
assert blink([125,17], 25) == 55312
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{blink(common.Loader.load_matrix(delimiter=" ",numeric=True)[0], 25)}{Back.RESET}{Fore.RESET}')

# Each number is "separate" so we can apply "backtracking" of steps and depth-first search!!!
# TBD
print(f'Part 2: {Back.GREEN}{Fore.BLACK}{blink(common.Loader.load_matrix(delimiter=" ",numeric=True)[0], 75)}{Back.RESET}{Fore.RESET}')


