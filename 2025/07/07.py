import common
from colorama import Fore,Back,Style

def run_tachyon(map):
    # Let's try naive
    # Find S in first line
    beams = dict.fromkeys([i for i in range(len(map[0]))], 0)
    beams[map[0].index('S')] = 1
    splits = 0
    for row in range(len(map)):
        # Go over beams and split any that you can
        new_beams = dict.fromkeys(beams.keys(), 0)
        for beam in beams:
            if beams[beam] > 0 and map[row][beam] == '^':
                splits += 1
                new_beams[beam - 1] += beams[beam]
                new_beams[beam + 1] += beams[beam]
            else:
                new_beams[beam] += beams[beam]
        beams = new_beams
    return splits, sum(beams.values())

def part_one(map):
    return run_tachyon(map)[0]

def part_two(map):
    return run_tachyon(map)[1]

assert part_one(common.Loader.load_matrix('test')) == 21
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_matrix('test')) == 40
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_matrix())}{Style.RESET_ALL}')