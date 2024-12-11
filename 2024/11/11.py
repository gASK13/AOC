import common
from colorama import Fore, Back

def blink_stones(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            stone_text = str(stone)
            half = len(stone_text) // 2
            new_stones.append(int(stone_text[:half]))
            new_stones.append(int(stone_text[half:]))
        else:
            new_stones.append(stone * 2024)
    return new_stones


def blink(stones, count):
    for i in range(count):
        stones = blink_stones(stones)
    return stones


assert blink_stones([0,1,10,99,999]) == [1, 2024, 1, 0, 9, 9, 2021976]
assert blink([125,17], 1) == [253000, 1, 7]
assert blink([125,17], 2) == [253, 0, 2024, 14168]
assert blink([125,17], 3) == [512072, 1, 20, 24, 28676032]
assert blink([125,17], 4) == [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]
assert blink([125,17], 5) == [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]
assert blink([125,17], 6) == [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]

assert len(blink([125,17], 25)) == 55312
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{len(blink(common.Loader.load_matrix(delimiter=" ",numeric=True)[0], 25))}{Back.RESET}{Fore.RESET}')

# Each number is "separate" so we can apply "backtracking" of steps and depth-first search!!!
# TBD
print(f'Part 2: {Back.GREEN}{Fore.BLACK}{len(blink(common.Loader.load_matrix(delimiter=" ",numeric=True)[0], 75))}{Back.RESET}{Fore.RESET}')


