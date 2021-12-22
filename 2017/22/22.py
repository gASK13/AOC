import common

# Clean = 0, Weakened = 1, Infected = 2, Flagged = 3

def run(file=None, cycles=10000, simple=True):
    map = common.Loader.load_matrix(file)
    map_of_map = {}
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                map_of_map[(x, y)] = 2

    carrier = [len(map[0]) // 2, len(map) // 2, (0, -1)]
    infection = 0
    for i in range(cycles):
        if (carrier[0], carrier[1]) not in map_of_map:
            map_of_map[(carrier[0], carrier[1])] = 0
        match map_of_map[(carrier[0], carrier[1])]:
            case 0:
                carrier[2] = (carrier[2][1], -carrier[2][0])
            case 2:
                carrier[2] = (-carrier[2][1], carrier[2][0])
            case 3:
                carrier[2] = (-carrier[2][0], -carrier[2][1])
        map_of_map[(carrier[0], carrier[1])] = (map_of_map[(carrier[0], carrier[1])] + (2 if simple else 1)) % 4
        infection += 1 if map_of_map[(carrier[0], carrier[1])] == 2 else 0
        carrier[0] += carrier[2][0]
        carrier[1] += carrier[2][1]
    return infection


assert run('test_map.txt', 70) == 41
assert run('test_map.txt', 100, simple=False) == 26
print(run('test_map.txt', 10000000, simple=False))
assert run('test_map.txt', 10000000, simple=False) == 2511944
assert run('test_map.txt') == 5587
print(f'REAL PT#1 {run()}')
print(f'REAL PT#2 {run(simple=False, cycles=10000000)}')
