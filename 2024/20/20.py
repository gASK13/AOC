import common
from colorama import Fore, Style, Back

def find_start(matrix):
    # find S position
    for idy, row in enumerate(matrix):
        if 'S' in row:
            return row.index('S'), idy

def find_end(matrix):
    # find E position
    for idy, row in enumerate(matrix):
        if 'E' in row:
            return row.index('E'), idy

def get_path_matrix(matrix, sx, sy):
    buffer = [(sx, sy, 0)]
    path_matrix = [[-1 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    seen = set()
    seen.add((sx, sy))
    while len(buffer) > 0:
        x, y, steps = buffer.pop(0)
        path_matrix[y][x] = steps
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in seen and 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[ny][nx] != '#':
                buffer.append((nx, ny, steps + 1))
                seen.add((nx, ny))
    return path_matrix

# PART TWO UPDATE:
# = We can cheat for up to 20 seconds
# = We should mark best path from each spot (!)
# = Then during the cheating round, we "radiate" from each wall and cheat for up to 20s in each direction in waves, finding any shortcuts

def find_cheats(matrix, cheat_duration=2):
    sx, sy = find_start(matrix)
    ex, ey = find_end(matrix)
    path_matrix = get_path_matrix(matrix, ex, ey)
    print(f'Path from {sx}/{sy} is {path_matrix[sy][sx]}')

    regular = path_matrix[sy][sx]

    buffer = [(sx, sy, 0)]
    cheats = {}

    seen = set()
    seen.add((sx, sy))

    while len(buffer) > 0:
        x, y, steps = buffer.pop(0)
        if matrix[y][x] == 'E':
            # can't be faster so we return
            return cheats
        for i in range(2, cheat_duration+1):
            # if it is 2, we just search one around this wall
            for j in range(0, i + 1):
                # start with (0,i) and (0,-i) and then go to (j, i-j) and (j, -i+j) and (-j, i-j) and (-j, -i+j)
                for cex, cey in [(x + j, y + i - j), (x - j, y + i - j), (x + j, y - i + j),
                                 (x - j, y - i + j)]:
                    if (cex, cey) not in seen and 0 <= cex < len(matrix) and 0 <= cey < len(matrix[0]) and matrix[cey][
                        cex] != '#':
                        ln = path_matrix[cey][cex]
                        if ln > -1 and ln + steps + i < regular:
                            # print(f'{Fore.GREEN}Found a cheat from {nx}, {ny} at {cex}, {cey} [{matrix[cey][cex]}] with {ln+steps+i+1} steps ({ln}).{Style.RESET_ALL}')
                            if (x, y, cex, cey) not in cheats:
                                cheats[(x, y, cex, cey)] = 0
                            cheats[(x, y, cex, cey)] = max(cheats[(x, y, cex, cey)], regular - (ln + steps + i))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in seen and 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[ny][nx] != '#':
                buffer.append((nx, ny, steps + 1))
                seen.add((nx, ny))

    return -1

def part_one(matrix, threshold=100):
    cheats = find_cheats(matrix)
    return sum([1 for c in cheats if cheats[c] >= threshold])

def part_two(matrix,threshold=100):
    cheats = find_cheats(matrix, 20)
    return sum([1 for c in cheats if cheats[c] >= threshold])


assert part_one(common.Loader.load_matrix('test'),0) == 44
assert part_one(common.Loader.load_matrix('test'),5) == 16
assert part_one(common.Loader.load_matrix('test'),10) == 10
assert part_one(common.Loader.load_matrix('test'),20) == 5
assert part_one(common.Loader.load_matrix('test'),40) == 2
assert part_one(common.Loader.load_matrix('test'),64) == 1

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_matrix())}{Style.RESET_ALL}')


assert part_two(common.Loader.load_matrix('test'), 76) == 3
assert part_two(common.Loader.load_matrix('test'), 74) == 7
assert part_two(common.Loader.load_matrix('test'), 72) == 29
assert part_two(common.Loader.load_matrix('test'), 70) == 41
assert part_two(common.Loader.load_matrix('test'), 68) == 55
assert part_two(common.Loader.load_matrix('test'), 66) == 67
assert part_two(common.Loader.load_matrix('test'), 64) == 86
assert part_two(common.Loader.load_matrix('test'), 62) == 106
assert part_two(common.Loader.load_matrix('test'), 60) == 129
assert part_two(common.Loader.load_matrix('test'), 58) == 154
assert part_two(common.Loader.load_matrix('test'), 56) == 193
assert part_two(common.Loader.load_matrix('test'), 54) == 222
assert part_two(common.Loader.load_matrix('test'), 52) == 253
assert part_two(common.Loader.load_matrix('test'), 50) == 285

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_matrix())}{Style.RESET_ALL}')
