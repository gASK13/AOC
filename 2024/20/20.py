import common
from colorama import Fore, Style, Back

def find_start(matrix):
    # find S position
    for idy, row in enumerate(matrix):
        if 'S' in row:
            return row.index('S'), idy

def find_path(matrix, sx, sy):
    buffer = [(sx, sy, 0)]
    seen = set()
    seen.add((sx, sy))
    while len(buffer) > 0:
        x, y, steps = buffer.pop(0)
        if matrix[y][x] == 'E':
            return steps
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in seen and 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[ny][nx] != '#':
                buffer.append((nx, ny, steps + 1))
                seen.add((nx, ny))
    return -1


def find_cheats(matrix):
    sx, sy = find_start(matrix)
    regular = find_path(matrix, sx, sy)
    print(f'Path from {sx}/{sy} is {regular}')

    buffer = [(sx, sy, 0)]
    cheats = {}

    seen = set()
    seen.add((sx, sy))

    while len(buffer) > 0:
        x, y, steps = buffer.pop(0)
        if matrix[y][x] == 'E':
            # can't be faster so we return
            return cheats
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in seen and 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]):
                if matrix[ny][nx] == '#':
                    for zx, zy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        cex, cey = nx + zx, ny + zy
                        if (cex, cey) not in seen and 0 <= cex < len(matrix) and 0 <= cey < len(matrix[0]) and matrix[cey][cex] != '#':
                            ln = find_path(matrix, cex, cey)
                            if ln > -1 and ln + steps + 2 < regular:
                                #print(f'{Fore.GREEN}Found a cheat from {nx}, {ny} at {cex}, {cey} [{matrix[cey][cex]}] with {ln+steps+2} steps ({ln}).{Style.RESET_ALL}')
                                cheats[(nx, ny, cex, cey)] = regular - (ln + steps + 2)
                    seen.add((nx, ny))
                else:
                    buffer.append((nx, ny, steps + 1))
                    seen.add((nx, ny))
    return -1

def part_one(matrix, threshold=100):
    cheats = find_cheats(matrix)
    return sum([1 for c in cheats if cheats[c] >= threshold])


assert part_one(common.Loader.load_matrix('test'),0) == 44
assert part_one(common.Loader.load_matrix('test'),5) == 16
assert part_one(common.Loader.load_matrix('test'),10) == 10
assert part_one(common.Loader.load_matrix('test'),20) == 5
assert part_one(common.Loader.load_matrix('test'),40) == 2
assert part_one(common.Loader.load_matrix('test'),64) == 1

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Style.RESET_ALL}')
