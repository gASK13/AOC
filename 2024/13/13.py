import common
from colorama import Fore, Back
import numpy as np

A = 3
B = 1

def solve_claw_machine(ax, ay, bx, by, px, py):
    i = np.array([[ax, bx], [ay, by]])
    o = np.array([px, py])
    solutions = np.linalg.solve(i, o)
    print(f'{ax}A + {bx}B = {px}')
    print(f'{ay}A + {by}B = {py}')
    print(f'A = {solutions[0]}, B = {solutions[1]}')
    if all([abs(s - round(s)) < 0.001 for s in solutions]):
        print(f'{solutions[0] * 3 + solutions[1]}')
        print(f'{round(solutions[0] * 3 + solutions[1])}')
        return round(solutions[0] * 3 + solutions[1])
    return 0

def part_one(lines):
    return solve(lines)

def solve(lines, offset=0):
    sum = 0
    while len(lines) > 0:
        ax, ay = [int(it[2:]) for it in lines.pop(0)[10:].split(', ')]
        bx, by = [int(it[2:]) for it in lines.pop(0)[10:].split(', ')]
        px, py = [int(it[2:]) for it in lines.pop(0)[7:].split(', ')]

        sum += solve_claw_machine(ax, ay, bx, by, px + offset, py + offset)

        while len(lines) > 0 and len(lines[0]) == 0:
            lines.pop(0)

    return sum


def part_two(lines):
    return solve(lines, 10000000000000)


assert part_one(common.Loader.load_lines('test')) == 480
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

assert part_two(common.Loader.load_lines('test')) == 459236326669 + 416082282239
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')