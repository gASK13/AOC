import common
from colorama import Fore, Back, Style

def count_adjacent_rolls(wh_map, x, y):
    if wh_map[x][y] != '@':
        return None
    return sum([1 if 0 <= x+dx < len(wh_map) and 0 <= y+dy < len(wh_map[0]) and wh_map[x+dx][y+dy] == '@' else 0 for dx in [-1, 0, 1] for dy in [-1, 0, 1]]) - 1

def translate_map(wh_map):
    _map = {'bySize' : {}, 'byCoords' : {}}
    for i in range(9):
        _map['bySize'][i] = []
    for x in range(len(wh_map)):
        for y in range(len(wh_map[0])):
            cnt = count_adjacent_rolls(wh_map, x, y)
            if cnt is None: continue
            _map['bySize'][cnt].append((x, y))
            _map['byCoords'][(x, y)] = cnt
    return _map

def part_one(original_map):
    wh_map = translate_map(original_map)
    return sum([len(wh_map['bySize'][i]) for i in range(4)])

def part_two(original_map):
    wh_map = translate_map(original_map)
    removed = 0
    while any([len(wh_map['bySize'][i]) > 0 for i in range(4)]):
        # take out all 4
        _to_process = wh_map['bySize'][3] + wh_map['bySize'][2] + wh_map['bySize'][1] + wh_map['bySize'][0]
        for i in range(4):
            wh_map['bySize'][i] = []
        for x,y in _to_process:
            removed += 1
            wh_map['byCoords'].pop((x,y))
        for x,y in _to_process:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (x+dx, y+dy) in wh_map['byCoords']:
                        wh_map['bySize'][wh_map['byCoords'][(x+dx, y+dy)]].remove((x+dx, y+dy))
                        wh_map['byCoords'][(x+dx, y+dy)] -= 1
                        wh_map['bySize'][wh_map['byCoords'][(x+dx, y+dy)]].append((x+dx, y+dy))
    return removed

assert part_one(common.Loader.load_matrix('test')) == 13
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_matrix('test')) == 43
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_matrix())}{Style.RESET_ALL}')