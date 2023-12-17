import common
from colorama import Fore, Back, Style


def store_position(x, y, heatloss, dx, dy, straight, map, seen, positions):
    if x < 0 or y < 0 or x >= len(map[0]) or y >= len(map):
        return
    if (x, y, dx, dy, straight) in seen and seen[(x, y, dx, dy, straight)] <= heatloss + map[y][x]:
        return
    seen[(x, y, dx, dy, straight)] = heatloss + map[y][x]
    positions.append((x, y, heatloss + map[y][x], dx, dy, straight))
    positions.sort(key=lambda _: _[2])


def ride_crucible(map, min=1, max=3, debug=False):
    # x, y, heatloss, dx, dy, straight
    positions = [(0, 0, 0, 0, 1, 0), (0, 0, 0, 1, 0, 0)]
    seen = {}
    while len(positions) > 0:
        x, y, heatloss, dx, dy, straight = positions.pop(0)

        if debug:
            print(f'At {x}, {y} with heatloss {heatloss} and length {straight}, coming in at {dx}, {dy}')
        # if we are at the end, return
        if x == len(map[0]) - 1 and y == len(map) - 1:
            if straight < min:
                continue # too short part :(
            print(f'Found path with heatloss {heatloss} and length {straight}, coming in at {dx}, {dy}')
            return heatloss

        # if we are not, try all possible directions (left, right, straight is straight < max)
        if straight < max:
            store_position(x + dx, y + dy, heatloss, dx, dy, straight + 1, map, seen, positions)
        # turn left and right
        if straight >= min:
            store_position(x - dy, y + dx, heatloss, -dy, dx, 1, map, seen, positions)
            store_position(x + dy, y - dx, heatloss, dy, -dx, 1, map, seen, positions)

    raise Exception('No path found')


assert ride_crucible(common.Loader.load_matrix('test', numeric=True)) == 102
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{ride_crucible(common.Loader.load_matrix(numeric=True))}')

assert ride_crucible(common.Loader.load_matrix('test', numeric=True), 4, 10) == 94
assert ride_crucible(common.Loader.load_matrix('test2', numeric=True), 4, 10) == 71

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{ride_crucible(common.Loader.load_matrix(numeric=True), 4, 10)}')