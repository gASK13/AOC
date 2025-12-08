import math

from colorama import Fore, Back, Style

import common


def run_simulation(coord_list, steps=None):
    # If steps is none, we run until we have full connection
    coords = {}
    distances = {}
    for idx, line in enumerate(coord_list):
        x,y,z = [int(i) for i in line.split(',')]
        coords[(x,y,z)] = idx

    # Make distances initial
    for ox,oy,oz in coords:
        for tx,ty,tz in coords:
            distance = math.sqrt(math.pow(abs(ox-tx), 2) + math.pow(abs(oy-ty),2) + math.pow(abs(oz-tz),2))
            if distance > 0 and (ox,oy,oz,tx,ty,tz) not in distances and (tx,ty,tz,ox,oy,oz) not in distances:
                distances[(ox,oy,oz,tx,ty,tz)] = distance

    distances = [(ox,oy,oz,tx,ty,tz,distance) for ((ox,oy,oz,tx,ty,tz),distance) in distances.items()]
    distances.sort(key=lambda x: x[6])

    i = 0
    while True:
        # Do not pop or find, just ... take it
        ox, oy, oz, tx, ty, tz, distance = distances[i]

        # First part - run for fixed number of steps
        if steps is not None and i >= steps:
            break
        i += 1

        # Merge partitions
        seen = set()
        if coords[ox,oy,oz] != coords[tx,ty,tz]:
            # Merge time!
            old_s = coords[tx,ty,tz]
            for ix,iy,iz in coords:
                if coords[ix,iy,iz] == old_s:
                    coords[ix,iy,iz] = coords[ox,oy,oz]
                seen.add(coords[ix,iy,iz])

        # Second part - run until fully connected
        # Yes, this can be 0 in case we did not merge anything - in that case we can't go to 1 partition
        if len(seen) == 1:
            return ox * tx

    sizes = [0 for _ in range(len(coords))]
    for ix, iy, iz in coords:
        sizes[coords[ix,iy,iz]] += 1
    sizes.sort()
    sizes = sizes[-3:]
    return sizes[0] * sizes[1] * sizes[2]

def part_one(coord_list, steps=1000):
    return run_simulation(coord_list, steps)

def part_two(coord_list):
    return run_simulation(coord_list)

assert part_one(common.Loader.load_lines('test'), 10) == 40
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test')) == 25272
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')