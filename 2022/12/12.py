import common
import re


def find_chars(input, char):
    results = []
    for x in range(len(input)):
        if char in input[x]:
            results += [(x, y.start()) for y in re.finditer(char, input[x])]
    return results


def find_path_inner(input, start, end):
    visited = {f'{start[0]}#{start[1]}': 0}
    buffer = [(start[0], start[1], 0)]
    while len(buffer) > 0:
        (x, y, ln) = buffer.pop(0)
        if x == end[0] and y == end[1]:
            return ln
        for (dx, dy) in [(x + 1, y + 0), (x + -1, y + 0), (x + 0, y + 1), (x + 0, y + -1)]:
            if len(input) > dx >= 0 and len(input[0]) > dy >= 0:
                if f'{dx}#{dy}' not in visited:
                    if ord(input[dx][dy]) <= ord(input[x][y]) + 1:
                        visited[f'{dx}#{dy}'] = ln + 1
                        buffer.append((dx, dy, ln + 1))
    return 999999


def find_best_path(input):
    starts = find_chars(input, 'S') + find_chars(input, 'a')
    end = find_chars(input, 'E')[0]
    for i in range(len(input)):
        input[i] = input[i].replace('E', 'z').replace('S', 'a')
    best = 999999
    for start in starts:
        new = find_path_inner(input, start, end)
        if new < best:
            best = new
    return best


def find_path(input):
    start = find_chars(input, 'S')[0]
    end = find_chars(input, 'E')[0]
    for i in range(len(input)):
        input[i] = input[i].replace('E', 'z').replace('S', 'a')
    return find_path_inner(input, start, end)


assert find_path(common.Loader.load_lines('test')) == 31
print(f'The path to climb has {find_path(common.Loader.load_lines())} steps')

assert find_best_path(common.Loader.load_lines('test')) == 29
print(f'The path to climb with variable start has {find_best_path(common.Loader.load_lines())} steps')
