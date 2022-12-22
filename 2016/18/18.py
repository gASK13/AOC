import common
from collections import Counter


def next_row(row):
    fillrow = f'.{row}.'
    patterns = ['^^.', '.^^', '^..', '..^']
    return ''.join(['^' if fillrow[i:i+3] in patterns else '.' for i in range(len(row))])


def count_safe_tiles(row, num):
    rows = []
    for i in range(num):
        rows.append(row)
        row = next_row(row)
    return Counter(''.join(rows))['.']

tests = [['..^^.', '.^^^^', '^^..^'],
['.^^.^.^^^^', '^^^...^..^', '^.^^.^.^^.', '..^^...^^^', '.^^^^.^^.^', '^^..^.^^..', '^^^^..^^^.', '^..^^^^.^^', '.^^^..^.^^', '^^.^^^..^^']]

for t in tests:
    for i in range(len(t) - 1):
        assert next_row(t[i]) == t[i+1]

assert count_safe_tiles('.^^.^.^^^^', 10) == 38
print(f'Safe tiles {count_safe_tiles(common.Loader.load_lines()[0], 40)}')
print(f'Safe tiles in 400k {count_safe_tiles(common.Loader.load_lines()[0], 400000)}')

