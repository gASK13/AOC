import common
from colorama import Fore, Style, Back

def parse(lines):
    locks = []
    keys = []
    buffer = []
    for line in lines:
        if len(line) == 0:
            item = [sum([1 for c in line if c == '#']) - 1 for line in common.transpose_matrix(buffer)]
            if buffer[0] == '#####':
                locks.append(item)
            else:
                keys.append(item)
            buffer = []
        else:
            buffer.append(line)
    item = [sum([1 for c in line if c == '#']) - 1 for line in common.transpose_matrix(buffer)]
    if buffer[0] == '#####':
        locks.append(item)
    else:
        keys.append(item)

    return locks, keys

def part_one(lines):
    locks, keys = parse(lines)
    print(f'Lock count: {len(locks)}; Key count: {len(keys)}')
    cnt = 0
    for lock in locks:
        for key in keys:
            if all([lock[i] + key[i] <= 5 for i in range(len(lock))]):
                cnt += 1
    return cnt

assert part_one(common.Loader.load_lines('test')) == 3
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')
