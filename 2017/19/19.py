import common


def get_path(original_map):
    _map = [f' {x} ' for x in original_map]
    _map.append(''.join([' ' for i in range(len(_map[-1]))]))
    y = 0
    x = _map[0].index('|')
    direction = {'x': 0, 'y': 1}
    path = ''
    steps = 1
    while True:
        if _map[y + direction['y']][x + direction['x']] == ' ':
            old_dir = direction
            direction = None
            for d in [{'x': -old_dir['y'], 'y': old_dir['x']}, {'x': old_dir['y'], 'y': -old_dir['x']}]:
                if _map[y + d['y']][x + d['x']] != ' ':
                    direction = d
            if direction is None:
                return path, steps
        if _map[y + direction['y']][x + direction['x']] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            path += _map[y + direction['y']][x + direction['x']]
        y += direction['y']
        x += direction['x']
        steps += 1


print(f'Test path {get_path(common.Loader.load_lines("test.txt", strip=False))} - expected ABCDEF / 38')
print(f'Real path {get_path(common.Loader.load_lines(strip=False))}')