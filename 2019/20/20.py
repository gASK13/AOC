import re
import copy


def update_template_for_part_two(_map):
    for x in range(0, len(_map[0])):
        for y in [0,1,-1,-2]:
            _map[y][x] = _map[y][x].lower()

    for y in range(0, len(_map)):
        for x in [0, 1, -1, -2]:
            _map[y][x] = _map[y][x].lower()


def update_outer_map(_map):
    # lines
    for x in range(0, len(_map[0])):
        if not re.match('(aa|zz|--)', get_pair(_map, x, 0)):
            _map[2][x] = '#'
        if not re.match('(aa|zz|--)', get_pair(_map, x, len(_map) - 2)):
            _map[-3][x] = '#'

    for y in range(0, len(_map)):
        if not re.match('(aa|zz|--)', get_pair(_map, 0, y)):
            _map[y][2] = '#'
        if not re.match('(aa|zz|--)', get_pair(_map, len(_map[0]) - 2, y)):
            _map[y][-3] = '#'


def pad_map(_map):
    side = max([len(line) for line in _map])
    for line in _map:
        if len(line) < side:
            for x in range(len(line), side):
                line.append(' ')


def print_map(_map):
    for row in _map:
        print(''.join(row))


def get_pair(_map, _x, _y):
    if re.match('[a-zA-Z]', _map[_y][_x]):
        for (dx, dy) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (0 <= _x + dx < len(_map[0])) & (0 <= _y + dy < len(_map)):
                if re.match('[a-zA-Z]', _map[_y + dy][_x + dx]):
                    return _map[min(_y, _y + dy)][min(_x, _x + dx)] + _map[max(_y, _y + dy)][max(_x, _x + dx)]

    return '--'


def locate_pair(_map, _pair):
    for (row, line) in enumerate(_map):
        for (index, char) in enumerate(line):
            if char == _pair[0]:
                if get_pair(_map, index, row) == _pair:
                    possible_exit = get_exit_for_pair(_map, index, row)
                    if possible_exit is not None:
                        return possible_exit

    return None


def get_exit_for_pair(_map, _x, _y):
    if _x + 1 < len(_map[0]):
        if re.match('[a-zA-Z]', _map[_y][_x + 1]):
            for dx in [-1, 2]:
                if (_x + dx >= 0) & (_x + dx < len(_map[0])):
                    if _map[_y][_x + dx] == '.':
                        return _x + dx, _y

    if _y + 1 < len(_map):
        if re.match('[a-zA-Z]', _map[_y + 1][_x]):
            for dy in [-1, 2]:
                if (_y + dy >= 0) & (_y + dy < len(_map)):
                    if _map[_y + dy][_x] == '.':
                        return _x, _y + dy

    return None


map = []
for line in open('20.txt', 'r').readlines():
    map.append([char for char in line.replace('\n', '')])
pad_map(map)
template = copy.deepcopy(map)

# PART ONE
x, y = locate_pair(map, 'ZZ')
map[y][x] = '!' # mark exit point for reference
x, y = locate_pair(map, 'AA')
map[y][x] = '@' # mark visited spaces

stack = [(x, y, 0)]
while len(stack) > 0:
    x, y, steps = stack.pop(0)
    for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (0 <= x + dx < len(map[0])) & (0 <= y + dy < len(map)):
            if map[y + dy][x + dx] == '.':
                map[y + dy][x + dx] = '@'
                stack.append((x + dx, y + dy, steps + 1))
            elif re.match('[a-zA-Z]', map[y + dy][x + dx]):
                pair = get_pair(map, x + dx, y + dy)
                p_exit = locate_pair(map, pair)
                if p_exit is not None:
                    if map[p_exit[1]][p_exit[0]] == '.':
                        map[p_exit[1]][p_exit[0]] = '@'
                        stack.append((p_exit[0], p_exit[1], steps + 1))
            elif map[y + dy][x + dx] == '!':
                print('Reached exit point in {} steps.'.format(steps + 1))
                stack.clear()
                break


# PART TWO
update_template_for_part_two(template)
map = copy.deepcopy(template)
update_outer_map(map)
x, y = locate_pair(map, 'zz')
map[y][x] = '!' # mark exit point for reference
template[y][x] = '#'
x, y = locate_pair(map, 'aa')
map[y][x] = '@' # mark visited spaces
template[y][x] = '#'
maps = [map]

stack = [(x, y, 0, 0)]
iter = 0
while len(stack) > 0:
    iter += 1
    if iter % 10000 == 0:
        print(stack)
    x, y, steps, level = stack.pop(0)
    level_map = maps[level]
    for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (0 <= x + dx < len(level_map[0])) & (0 <= y + dy < len(level_map)):
            if level_map[y + dy][x + dx] == '.':
                level_map[y + dy][x + dx] = '@'
                stack.append((x + dx, y + dy, steps + 1, level))
            elif re.match('[A-Z]', map[y + dy][x + dx]):
                if len(maps) == level + 1:
                    maps.append(copy.deepcopy(template))
                next_map = maps[level + 1]
                pair = get_pair(level_map, x + dx, y + dy)
                p_exit = locate_pair(next_map, pair.lower())
                if p_exit is not None:
                    if next_map[p_exit[1]][p_exit[0]] == '.':
                        next_map[p_exit[1]][p_exit[0]] = '@'
                        stack.append((p_exit[0], p_exit[1], steps + 1, level + 1))
            elif re.match('[a-z]', map[y + dy][x + dx]):
                prev_map = maps[level - 1]
                pair = get_pair(level_map, x + dx, y + dy)
                p_exit = locate_pair(prev_map, pair.upper())
                if p_exit is not None:
                    if prev_map[p_exit[1]][p_exit[0]] == '.':
                        prev_map[p_exit[1]][p_exit[0]] = '@'
                        stack.append((p_exit[0], p_exit[1], steps + 1, level - 1))
            elif level_map[y + dy][x + dx] == '!':
                print('Reached looped maze exit point in {} steps.'.format(steps + 1))
                stack.clear()
                break
