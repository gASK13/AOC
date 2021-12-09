import common


def multiply(list):
    t = 1
    for i in list:
        t *= i
    return t


def get_neighbours(_data, _x, _y):
    n = []
    if _x - 1 >= 0:
        n.append((_data[_x - 1][_y], _x - 1, _y))
    if _x + 1 < len(_data):
        n.append((_data[_x + 1][_y], _x + 1, _y))
    if _y - 1 >= 0:
        n.append((_data[_x][_y - 1], _x, _y -1))
    if _y + 1 < len(_data[0]):
        n.append((_data[_x][_y + 1], _x, _y + 1))
    return n


def get_basin_size(_data, i, j):
    #recursively go around until you hit 9 or visited field
    #set all visited to 9 (to avoid double hits)
    buffer = [(i, j)]
    _data[i][j] = 9
    size = 0
    while len(buffer) > 0:
        item = buffer.pop()
        size += 1
        for n in get_neighbours(_data, item[0], item[1]):
            if n[0] < 9:
                _data[n[1]][n[2]] = 9
                buffer.append((n[1], n[2]))
    return size


def find_low_points(_data):
    lows = []
    for i in range(len(_data)):
        for j in range(len(_data[0])):
            if all([_data[i][j] < n[0] for n in get_neighbours(_data, i, j)]):
                lows.append((_data[i][j], i, j, get_basin_size(_data, i, j)))
    print(lows)
    return lows


data = common.Loader.load_matrix('text.txt', numeric=True)
low_points = find_low_points(data)
print('Lows: {}'.format(sum([i[0] + 1 for i in low_points])))
print('Basin size (*): {}'.format(multiply(sorted([i[3] for i in low_points], reverse=True)[:3])))

data = common.Loader.load_matrix(numeric=True)
low_points = find_low_points(data)
print('Lows: {}'.format(sum([i[0] + 1 for i in low_points])))
print('Basin size (*): {}'.format(multiply(sorted([i[3] for i in low_points], reverse=True)[:3])))

