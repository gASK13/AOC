import common


def unfold_map(_map):
    return [[(x + i + j) % 10 + (x + i + j) // 10 for i in range(5) for x in line] for j in range(5) for line in _map]


def find_path(_map):
    paths = {(0, 0): 0}
    buffer = [(0, 0, 0)]
    while len(buffer) > 0 and (len(_map) - 1, len(_map[0]) - 1) not in paths:
        x, y, path_len = buffer.pop()
        for dx, dy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            cur_len = paths[(x, y)]
            if 0 <= dx < len(_map) and 0 <= dy < len(_map[0]) \
                    and ((dx, dy) not in paths or cur_len + _map[dx][dy] < paths[(dx, dy)]):
                paths[(dx, dy)] = cur_len + _map[dx][dy]
                buffer.append((dx, dy, cur_len + _map[dx][dy]))
        buffer.sort(key=lambda tup: tup[2], reverse=True)
    return paths[(len(_map) - 1, len(_map[0]) - 1)]


map = common.Loader.load_matrix('test.txt', numeric=True)
print(f'Path in test = {find_path(map)} (expected 40)')
print(f'Real path = {find_path(common.Loader.load_matrix(numeric=True))}')

print(f'Path in test = {find_path(unfold_map(map))} (expected 315)')
print(f'Real path = {find_path(unfold_map(common.Loader.load_matrix(numeric=True)))}')
