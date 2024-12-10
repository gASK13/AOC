import common
from colorama import Fore, Back

def find_all_trailheads(matrix):
    trailheads = []
    for idy, line in enumerate(matrix):
        for idx, item in enumerate(line):
            if item == '0':
                summits = find_summits(matrix, idx, idy)
                if len(summits) > 0:
                    trailheads.append((idx, idy, summits))
    return trailheads

def find_summits(matrix, x, y):
    summits = {}
    buffer = [(x, y)]
    while len(buffer) > 0:
        x, y = buffer.pop()
        val = int(matrix[y][x])
        if matrix[y][x] == '9':
            if (x, y) not in summits:
                summits[(x, y)] = 0
            summits[(x, y)] += 1
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx = x + dx
            ny = y + dy
            if len(matrix) > ny >= 0 and len(matrix[0]) > nx >= 0:
                if matrix[ny][nx] != '.' and int(matrix[ny][nx]) == val + 1:
                    buffer.append((nx, ny))
    return summits

def part_one(matrix):
    return sum([len(s.keys()) for x,y,s in find_all_trailheads(matrix)])


def part_two(matrix):
    return sum([sum(s.values()) for x, y, s in find_all_trailheads(matrix)])


for i in [1,2,3,4,36]:
    assert part_one(common.Loader.load_matrix(f"test_{i}")) == i

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Fore.RESET}{Back.RESET}')


for i in [3,13,81,227]:
    assert part_two(common.Loader.load_matrix(f"test2_{i}")) == i

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_matrix())}{Fore.RESET}{Back.RESET}')

