import common
from colorama import Fore, Back, Style

def part_one(lines):
    return find_paths(lines, 'you', 'out')

def part_two(lines):
    # Simple optimization? Count subpaths (since we know the stops)
    # Next step - count all paths from all nodes to all other nodes recursively (span from out?)
    way1 = find_paths(lines, 'svr', 'fft') * find_paths(lines, 'fft', 'dac') * find_paths(lines, 'dac', 'out')
    way2 = find_paths(lines, 'svr', 'dac') * find_paths(lines, 'dac', 'fft') * find_paths(lines, 'fft', 'out')
    return way1 + way2

def find_paths(lines, start, end):
    paths = {}
    goals = set()
    for line in lines:
        paths[line.split(':')[0]] = { 'targets' : [], 'paths' : 0 }
        paths[line.split(':')[0]]['targets'] = line.split(': ')[1].split(' ')
        goals = goals.union(set(paths[line.split(':')[0]]['targets']))

    # overwrite end and start!
    paths[end] = { 'targets' : [], 'paths' : 1 }
    # cut all other dead-ends!
    while True:
        candidate = None
        for goal in goals:
            if goal not in paths:
                candidate = goal
                break
        if candidate is None:
            break
        else:
            goals.remove(candidate)
            for path in paths:
                if candidate in paths[path]['targets']:
                    paths[path]['targets'].remove(candidate)

    while True:
        candidate = None
        for p in paths:
            if len(paths[p]['targets']) == 0:
                candidate = p
                break

        if candidate is None or candidate == start:
            # no more paths?
            return paths[start]['paths']

        paths_cnt = paths[candidate]['paths']
        paths.pop(candidate)
        for path in paths:
            if candidate in paths[path]['targets']:
                paths[path]['targets'].remove(candidate)
                paths[path]['paths'] += paths_cnt

assert part_one(common.Loader.load_lines('test')) == 5
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test2')) == 2
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')