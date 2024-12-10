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
    summits = set()
    buffer = [(x, y)]
    while len(buffer) > 0:
        x, y = buffer.pop()
        val = int(matrix[y][x])
        if matrix[y][x] == '9':
            summits.add((x, y))
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx = x + dx
            ny = y + dy
            if len(matrix) > ny >= 0 and len(matrix[0]) > nx >= 0:
                if matrix[ny][nx] != '.' and int(matrix[ny][nx]) == val + 1:
                    buffer.append((nx, ny))
    return summits

def part_one(matrix):
    return sum([len(s) for x,y,s in find_all_trailheads(matrix)])

for i in [1,2,3,4,36]:
    assert part_one(common.Loader.load_matrix(f"test_{i}")) == i

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Fore.RESET}{Back.RESET}')

