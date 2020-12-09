import copy

# This function computes GCD
def compute_gcd(_a, _b):
   while _b:
       _a, _b = _b, _a % _b
   return abs(_a)


def print_map(_map):
    for row in _map:
        print(''.join(row))


def compute_map(_x, _y, _map):
    if _map[_y][_x] != '#':
        return 0
    _map[_y][_x] = '@'
    for ey in range(0, len(_map)):
        for ex in range(0, len(_map[0])):
            if _map[ey][ex] == '#':
                shadow(_x, _y, ex, ey, _map)

    return count_chars('#', _map)


def deltas(_x, _y, _tx, _ty):
    dx = _tx - _x
    dy = _ty - _y
    while True:
        gcd = compute_gcd(dx, dy)
        if gcd == 1:
            break
        dx = int(dx / gcd)
        dy = int(dy / gcd)
    return dx, dy


def shadow(_x, _y, _ex, _ey, _map):
    dx, dy = deltas(_x, _y, _ex, _ey)

    cx = _ex + dx
    cy = _ey + dy
    while (cx >= 0) & (cy >= 0) & (cx < len(_map[0])) & (cy < len(_map)):
        _map[cy][cx] = 'X'
        cx += dx
        cy += dy


def count_chars(_char, _map):
    cnt = 0
    for row in _map:
        for char in row:
            if char == _char:
                cnt += 1
    return cnt


def shoot(_x, _y, _tx, _ty, _map):
    dx, dy = deltas(_x, _y, _tx, _ty)

    cx = _x + dx
    cy = _y + dy
    while (cx >= 0) & (cy >= 0) & (cx < len(_map[0])) & (cy < len(_map)):
        if _map[cy][cx] == '#':
            _map[cy][cx] = '.'
            return cx, cy
        cx += dx
        cy += dy

    return None


def step(_x, _y, _map):
    if _x == 0:
        if _y == 0:
            return 1, 0
        return 0, _y - 1
    if _x == len(_map[0]) - 1:
        if _y == len(_map) - 1:
            return _x - 1, _y
        return _x, _y + 1
    if _y == 0:
        return _x + 1, _y
    if _y == len(_map) - 1:
        return _x - 1, _y


def compute_fractions(_numerator, _denominator, switch = False):
    fracs = set()
    for den in range(min(2, _denominator + 1), max(_denominator, -1)):
        for num in range(min(_numerator * abs(den), (_numerator + 1) * abs(den)) + 1, max(_numerator * abs(den), (_numerator + 1) * abs(den))):
            div = compute_gcd(abs(num), abs(_denominator * den))
            if div > 1:
                if abs((_denominator * den) / div) < abs(_denominator):
                    if switch:
                        fracs.add((int(_denominator * abs(den) / div), int(num / div)))
                    else:
                        fracs.add((int(num / div), int(_denominator * abs(den) / div)))

    # SORT !
    sorted = []
    for item in fracs:
        sorted.append(item)
    sorted.sort(key=lambda x:x[0]/x[1], reverse=True)

    return sorted


def get_steps_for(_x, _y, _cx, _cy, _nx, _ny, _map):
    steps = [(_cx, _cy)]

    # if DX/DY == 0 -> return just this (division by 0)
    if (_cx - _x == 0) | (_cy - _y == 0) | (_nx - _x == 0) | (_ny - _y == 0):
        return steps

    # get all "substeps" based on length to _cx, _cy
    if _cx == _nx:
        denominator = _cx - _x
        fractions = compute_fractions(min(_cy - _y, _ny - _y), denominator, True)
        for fraction in fractions:
            steps.append((_x + fraction[0], _y + fraction[1]))
    if _cy == _ny:
        denominator = _cy - _y
        fractions = compute_fractions(min(_cx - _x, _nx - _x), denominator)
        for fraction in fractions:
            steps.append((_x + fraction[0], _y + fraction[1]))

    return steps


def vaporizaton(_x, _y, _map):
    _map[_y][_x] = '@'
    vaporized = []
    cx = _x
    cy = 0
    while count_chars('#', _map) > 0:
        nx, ny = step(cx, cy, _map)
        for _step in get_steps_for(_x, _y, cx, cy, nx, ny, _map):
            hit = shoot(_x, _y, _step[0], _step[1], _map)
            if hit is not None:
                vaporized.append(hit)
        cx, cy = nx, ny

    return vaporized

space_map = []
for line in open('10.txt', 'r').readlines():
    space_map.append([char for char in line.strip()])

# PREVIEW
print('\n - - - - - - - - - - - - ')
print_map(space_map)

#PART ONE
print('\n - - - - - - - - - - - - ')
max_map = (None, None, 0)
for y in range(0, len(space_map)):
    for x in range(0, len(space_map[0])):
        work_map = copy.deepcopy(space_map)
        ret = compute_map(x, y, work_map)
        if ret > max_map[2]:
            max_map = (x, y, ret)

print(max_map)

#PART TWO
print('\n - - - - - - - - - - - - ')
vap = vaporizaton(max_map[0], max_map[1], space_map)
print(vap)
#print(len(vap))
#print(vap[0], vap[1], vap[2], vap[9], vap[19], vap[49], vap[99],  vap[198], vap[199], vap[200], vap[298])
print(vap[199])
#print([(8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2), (15, 1), (12, 2), (13, 2), (14, 2), (15, 2), (12, 3), (16, 4), (15, 4), (10, 4), (4, 4), (2, 4), (2, 3), (0, 2), (1, 2), (0, 1), (1, 1), (5, 2), (1, 0), (5, 1), (6, 1), (6, 0), (7, 0), (8, 0), (10, 1), (14, 0), (16, 1), (13, 3), (14, 3)])

