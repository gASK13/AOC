import common
from colorama import Fore, Back

#rrbgbr can be made in 4 ways!!!
#gbbr can be made in 2 ways!!!
def can_be_made(line, parts, full_parts, negatives):
    if line in negatives:
        return 0
    if len(line) == 0:
        return 1
    if line in full_parts:
        return full_parts[line]

    cnt = 0
    for part in parts:
        if part == line[:len(part)]:
            opts = can_be_made(line[len(part):], parts, full_parts, negatives)
            # 'rgr' would be 'r+g+r' but aldo 'rg+r' and possible 'r+gr' based on how I did it, but it is NOT originals
            if opts > 0:
                cnt += opts

    if cnt > 0:
        full_parts[line] = cnt
        return cnt

    negatives.add(line)
    return 0

def compute(lines):
    parts = {}
    full_parts = {}
    for l in lines.pop(0).split(', '):
        parts[l] = 1
    negatives = set()

    lines.pop(0)

    ctr = 0
    sum = 0
    for line in lines:
        c = can_be_made(line, parts, full_parts, negatives)
        if c > 0:
            ctr += 1
            sum += c

    return ctr, sum

def part_one(lines):
    return compute(lines)[0]

def part_two(lines):
    return compute(lines)[1]


assert part_one(common.Loader.load_lines('test')) == 6
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

assert part_two(common.Loader.load_lines('test')) == 16
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')