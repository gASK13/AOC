from numpy.matlib import zeros

import common
from colorama import Fore,Back,Style



def part_one(lines):
    dial = 50
    size = 100
    zeroes = 0
    for line in lines:
        move = int(line[1:])
        move *= -1 if line[0] == 'L' else 1
        dial = (dial + move) % size
        if dial == 0:
            zeroes += 1
    return zeroes

def part_two(lines):
    dial = 50
    size = 100
    zeroes = 0
    for line in lines:
        move = int(line[1:])
        move *= -1 if line[0] == 'L' else 1
        was_zero = dial == 0
        dial += move
        while dial < 0:
            dial += size
            if not was_zero:
                zeroes += 1
            else:
                was_zero = False
        if dial == 0:
            zeroes += 1
        while dial >= size:
            dial -= size
            zeroes += 1
    print(zeroes)
    return zeroes

assert part_one(common.Loader.load_lines('test')) == 3
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test')) == 6
assert part_two(common.Loader.load_lines('test2')) == 7
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')

# 5544 < TOO LOW?
