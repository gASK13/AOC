def build_level():
    return [['.' for x in range(0, 5)] for y in range(0, 5)]


def parse_map(_file):
    map = []
    for line in open(_file, 'r').readlines():
        map.append([char for char in line.strip()])
    return map


def print_map(_map):
    for key in _map.keys():
        print('Level {}'.format(key))
        print(hash_map(_map[key], '\n'))


def hash_map(_map, _char=''):
    return _char.join([''.join(line) for line in _map])


def biodiversity(_map):
    bio = 0
    for key in _map.keys():
        for line in _map[key]:
            for char in line:
                if char == '#':
                    bio += 1
    return bio


def step(_map):
    counts = {}
    fill_levels = set()
    for z in _map.keys():
        for (y, line) in enumerate(_map[z]):
            for (x, char) in enumerate(line):
                if char == '#':
                    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if (0 <= x + dx < len(line)) & (0 <= y + dy < len(_map[z])) & ((y + dy != 2) | (x + dx != 2)):
                            if (z, y + dy, x + dx) not in counts:
                                counts[(z, y + dy, x + dx)] = 0
                            counts[(z, y + dy, x + dx)] += 1
                        elif (y + dy == 2) & (x + dx == 2):
                            if z - 1 not in _map:
                                fill_levels.add(z - 1)
                            if dy != 0:
                                for ddx in range(0, 5):
                                    if (z - 1, 0 if dy == 1 else 4, ddx) not in counts:
                                        counts[(z - 1, 0 if dy == 1 else 4, ddx)] = 0
                                    counts[(z - 1, 0 if dy == 1 else 4, ddx)] += 1
                            else:
                                for ddy in range(0, 5):
                                    if (z - 1, ddy, 0 if dx == 1 else 4) not in counts:
                                        counts[(z - 1, ddy, 0 if dx == 1 else 4)] = 0
                                    counts[(z - 1, ddy, 0 if dx == 1 else 4)] += 1
                        else:
                            if z + 1 not in _map:
                                fill_levels.add(z + 1)
                            if (z + 1, 2 + dy, 2 + dx) not in counts:
                                counts[(z + 1, 2 + dy, 2 + dx)] = 0
                            counts[(z + 1, 2 + dy, 2 + dx)] += 1

    for z in fill_levels:
        _map[z] = build_level()

    for z in _map.keys():
        for (y, line) in enumerate(_map[z]):
            for (x, char) in enumerate(line):
                if (z, y, x) not in counts:
                    counts[(z, y, x)] = 0
                if (char == '#') & (counts[(z, y, x)] != 1):
                    line[x] = '.'
                elif (char == '.') & (1 <= counts[(z, y, x)] <= 2):
                    line[x] = '#'

map = {}
map[0] = parse_map('24.txt')
print_map(map)

for i in range(0, 200):
    step(map)
    print('\n{} minute'.format(i))
    print_map(map)

print(biodiversity(map))