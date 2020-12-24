def init_floor(_file_name):
    hexes = {}
    for line in open(_file_name, 'r').readlines():
        modifier = 0
        pos = (0, 0)
        for char in line.strip():
            if (char == 'n') | (char == 's'):
                modifier = -1 if char == 'n' else 1
            else:
                dx = -1 if char == 'w' else 1
                if modifier != 0:
                    dx = 0 if modifier == dx else dx
                dy = modifier
                pos = (pos[0] + dx, pos[1] + dy)
                modifier = 0
        if pos not in hexes:
            hexes[pos] = 'BLACK'
        else:
            del hexes[pos]
    return hexes


def end_day(_floor):
    counts = {}
    for tile in _floor:
        if tile not in counts:
            counts[tile] = 0
        for (dx, dy) in [(1, 0), (-1, 0), (0, -1), (1, -1), (0, 1), (-1, 1)]:
            n_pos = (tile[0] + dx, tile[1] + dy)
            if n_pos not in counts:
                counts[n_pos] = 0
            counts[n_pos] += 1

    for tile in counts:
        if (tile in _floor) & (counts[tile] == 0):
            del _floor[tile]
        elif (tile in _floor) & (counts[tile] > 2):
            del _floor[tile]
        elif (tile not in _floor) & (counts[tile] == 2):
            _floor[tile] = 'BLACK'


floor = init_floor('24.txt')
print('Start: {}'.format(len(floor)))
for day in range(1, 101):
    end_day(floor)
    if day % 10 == 0:
        print('Day {}: {}'.format(day, len(floor)))
