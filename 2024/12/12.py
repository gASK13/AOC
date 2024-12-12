import common
from colorama import Fore, Back

def map_plot(matrix, px, py):
    buffer = [(px, py)]
    plot = set()
    char = matrix[py][px]
    while len(buffer) > 0:
        x, y = buffer.pop()
        if matrix[y][x] == char:
            plot.add((x, y))
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in plot and 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix) and matrix[ny][nx] == char and (nx, ny) not in plot:
                    buffer.append((nx, ny))
    return plot

def compute_fence(plot):
    area = len(plot)
    circ = 0
    for x, y in plot:
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            if (x + dx, y + dy) not in plot:
                circ += 1
    return circ * area

def part_one(matrix):
    plotted = set()
    sums = 0
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if (x, y) not in plotted:
                plot = map_plot(matrix, x, y)
                plotted = plotted.union(plot)
                sums += compute_fence(plot)
    return sums

assert part_one(common.Loader.load_matrix('test_A')) == 140
assert part_one(common.Loader.load_matrix('test_O')) == 772
assert part_one(common.Loader.load_matrix('test_big')) == 1930

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Fore.RESET}{Back.RESET}')