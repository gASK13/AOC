def parse_map(_file):
    map = []
    for line in open(_file, 'r').readlines():
        map.append([char for char in line.strip()])
    return map


def print_map(_map):
    print(hash_map(_map, '\n'))


def hash_map(_map, _char=''):
    return _char.join([''.join(line) for line in _map])


def biodiversity(_map):
    val = 1
    bio = 0
    for line in _map:
        for char in line:
            if char == '#':
                bio += val
            val *= 2
    return bio


def step(_map):
    count_map = [[0 for c in line] for line in _map]
    for (y, line) in enumerate(_map):
        for (x, char) in enumerate(line):
            if char == '#':
                for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if (0 <= x + dx < len(line)) & (0 <= y + dy < len(_map)):
                        count_map[y + dy][x + dx] += 1

    for (y, line) in enumerate(_map):
        for (x, char) in enumerate(line):
            if (char == '#') & (count_map[y][x] != 1):
                line[x] = '.'
            elif (char == '.') & (1 <= count_map[y][x] <= 2):
                line[x] = '#'


map = parse_map('24.txt')
hashes = {hash_map(map)}
print('init')
print_map(map)
i = 0
while True:
    i += 1
    step(map)
    h = hash_map(map)
    print('\n{} minute'.format(i))
    print_map(map)
    if h in hashes:
        print('WOOT!')
        print(biodiversity(map))
        break
    else:
        hashes.add(hash_map(map))
