import copy


def print_map(_map):
    print('\n\n')
    for line in _map:
        print(''.join([item for item in line]))


def print_result(map):
    cnt = 0
    for line in map:
        for char in line:
            if char == '#':
                cnt += 1
    print('\n\nOCCUPIED {}'.format(cnt))

def run_round(_map, simple=True):
    old_map = copy.deepcopy(_map)
    changed = False
    for (y, line) in enumerate(_map):
        for (x, char) in enumerate(line):
            if simple:
                occ = count_occupied(x, y, old_map)
            else:
                occ = count_occupied_complex(x, y, old_map)
            if (old_map[y][x] == 'L') & (occ == 0):
                _map[y][x] = '#'
                changed = True
            if (old_map[y][x] == '#') & (occ >= (4 if simple else 5)):
                _map[y][x] = 'L'
                changed = True
    return changed


def count_occupied_complex(_x, _y, _map):
    cnt = 0
    for (dx, dy) in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
        if (dx != 0) | (dy != 0):
            x = _x + dx
            y = _y + dy
            while (0 <= x < len(_map[0])) & (0 <= y < len(_map)):
                if _map[y][x] == '#':
                    cnt += 1
                    break
                elif _map[y][x] == 'L':
                    break
                else:
                    x += dx
                    y += dy
    return cnt

def count_occupied(_x, _y, _map):
    cnt = 0
    for (x, y) in [(_x + x, _y + y) for x in range(-1, 2) for y in range(-1, 2)]:
        if ((x != _x) | (y != _y)) & (0 <= x < len(_map[0])) & (0 <= y < len(_map)):
            if _map[y][x] == '#':
                cnt += 1
    return cnt


#PART ONE
map = []
for line in open('11.txt', 'r').readlines():
    map.append([char for char in line.strip()])
complex_map = copy.deepcopy(map)

# PART ONE
print_map(map)
while run_round(map):
    print_map(map)
print_map(map)
print_result(map)

# PART TWO
print_map(complex_map)
while run_round(complex_map, simple=False):
    print_map(complex_map)
print_map(complex_map)
print_result(complex_map)