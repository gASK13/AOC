import common

def count_houses(instructions, robo=False):
    visited = set()
    visited.add((0, 0))
    curr = [(0, 0)] if not robo else [(0, 0), (0, 0)]
    moves = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
    for i in instructions:
        x, y = curr.pop(0)
        x, y = x + moves[i][0], y + moves[i][1]
        visited.add((x, y))
        curr.append((x, y))
    return len(visited)

test_data = {'>' : (2, 2), '^>v<': (4, 3), '^v^v^v^v^v': (2, 11), '^v': (2, 3)}
for t in test_data:
    assert count_houses(t) == test_data[t][0]
    assert count_houses(t, True) == test_data[t][1]

print(f'Visited houses: {count_houses(common.Loader.load_lines()[0])}')
print(f'Visited houses (ROBO version): {count_houses(common.Loader.load_lines()[0], True)}')