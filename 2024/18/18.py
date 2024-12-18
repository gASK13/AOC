import common
from colorama import Fore, Back
from tqdm import tqdm

def part_one(lines, xit=(70,70), limit=1024):
    obstacles = []
    for line in lines[:limit]:
        x, y = [int(_) for _ in line.split(',')]
        obstacles.append((x,y))
    return find_path(obstacles, xit)

def find_path(obstacles, xit):
    # now to find path
    buffer = [(0,0,0,[(0,0)])]
    seen = set()
    seen.add((0,0))
    while len(buffer) > 0:
        x, y, p, path = buffer.pop(0)
        if (x,y) == xit:
            return p
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if 0 <= x+dx <= xit[0] and 0 <= y+dy <= xit[1]:
                if (x+dx, y+dy) not in obstacles:
                    if (x+dx, y+dy) not in seen:
                        buffer.append((x+dx,y+dy,p+1, path+[(x+dx,y+dy)]))
                        seen.add((x+dx, y+dy))

    return -1


def part_two(lines, xit=(70,70), limit=1024):
    obstacles = []
    for i in tqdm(range(len(lines))):
        x, y = [int(_) for _ in lines[i].split(',')]
        obstacles.append((x, y))
        if i > limit:
            if find_path(obstacles, xit) == -1:
                # no path
                return x, y
    return None



assert part_one(common.Loader.load_lines('test'), (6,6), 12) == 22
print(f'Part 1:{Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

assert part_two(common.Loader.load_lines('test'), (6,6), 12) == (6, 1)
print(f'Part 2:{Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

