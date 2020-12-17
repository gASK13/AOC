def get_around(_x, _y, _z):
    ret = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                ret.append((_x + dx, _y + dy, _z + dz))
    ret.remove((_x + 0, _y + 0, _z + 0))
    return ret


def add_around(_x, _y, _z, _count_map):
    for cx, cy, cz in get_around(_x, _y, _z):
        if (cx, cy, cz) not in _count_map:
            _count_map[(cx, cy, cz)] = 1
        else:
            _count_map[(cx, cy, cz)] += 1


def run_generation(_map):
    count_map = {}
    for x, y, z in _map.keys():
        add_around(x, y, z, count_map)

    new_map = {}
    for (x, y, z), cnt in count_map.items():
        if cnt == 3:
            new_map[(x, y, z)] = True
        elif ((x, y, z) in _map) & (2 <= cnt <= 3):
            new_map[(x, y, z)] = True

    return new_map


map = {}
for (row, line) in enumerate(open('17.txt', 'r').readlines()):
    for (idx, char) in enumerate(line.strip()):
        if char == '#':
            map[(idx, row, 0)] = True

for i in range(0, 6):
    map = run_generation(map)
    print('Step {}: Size {}'.format(i, len(map)))


