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

def simple_price(plot):
    area = len(plot)
    circ = 0
    for x, y in plot:
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            if (x + dx, y + dy) not in plot:
                circ += 1
    return circ * area

def bulk_discount(plot):
    area = len(plot)
    corners = 0
    # don't count sides, count corners!
    # it should be the same count!
    for x, y in plot:
        # count neighbors
        nc = sum([1 for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)] if (x + dx, y + dy) in plot])
        # for 2 and 3 and 4, we can have corners according to logic below
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            if (x + dx, y) in plot and (x, y + dy) in plot:
                # bottom right is not in
                if (x - dx, y) not in plot and (x, y - dy) not in plot:
                    corners += 1
                # topleft is not int
                if (x + dx, y + dy) not in plot:
                    corners += 1
        if nc == 1:
            # this is "sole edge" and has 2 corners
            corners += 2

        if nc == 0:
            # sole box
            corners += 4

    return corners * area

def get_cost(matrix, cost_function):
    plotted = set()
    sums = 0
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if (x, y) not in plotted:
                plot = map_plot(matrix, x, y)
                plotted = plotted.union(plot)
                sums += cost_function(plot)
    return sums


def part_one(matrix):
    return get_cost(matrix, simple_price)

def part_two(matrix):
    return get_cost(matrix, bulk_discount)

assert part_one(common.Loader.load_matrix('test_A')) == 140
assert part_one(common.Loader.load_matrix('test_O')) == 772
assert part_one(common.Loader.load_matrix('test_big')) == 1930

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Fore.RESET}{Back.RESET}')


assert part_two(common.Loader.load_matrix('test_A')) == 80
assert part_two(common.Loader.load_matrix('test_O')) == 436
assert part_two(common.Loader.load_matrix('test_E')) == 236
assert part_two(common.Loader.load_matrix('test_B')) == 368
assert part_two(common.Loader.load_matrix('test_big')) == 1206

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_matrix())}{Fore.RESET}{Back.RESET}')
