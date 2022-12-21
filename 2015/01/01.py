import common
from collections import Counter


def floor_count(line):
    c = Counter(line)
    return c['('] - c[')']


def basement_entrance(line):
    i = 0
    for (idx, c) in enumerate(line):
        i += 1 if c == '(' else -1
        if i == -1:
            return idx + 1
    return None


test_data = {'(())': 0, '()()': 0, '(((': 3, '(()(()(': 3, '))(((((': 3, '())': -1, '))(': -1, ')))': -3, ')())())': -3}

for t in test_data:
    assert floor_count(t) == test_data[t]

print(f'Real floor is {floor_count(common.Loader.load_lines()[0])}')

test_two = {')' : 1, '()())': 5, '(': None}
for t in test_two:
    assert basement_entrance(t) == test_two[t]

print(f'Basement entered at {basement_entrance(common.Loader.load_lines()[0])}')
