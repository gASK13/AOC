import common
from colorama import Fore, Back, Style

def part_one(lines):
    paths = {}
    for line in lines:
        paths[line.split(':')[0]] = line.split(': ')[1].split(' ')

    buffer = ['you']
    cnt = 0
    while len(buffer) > 0:
        where = buffer.pop(0)
        for path in paths[where]:
            if path == 'out':
                cnt += 1
            else:
                buffer.append(path)
    return cnt

assert part_one(common.Loader.load_lines('test')) == 5
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')