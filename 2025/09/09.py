import common
from colorama import Fore, Back, Style

def part_one(tiles):
    _tiles = [[int(i) for i in tile.split(',')] for tile in tiles]
    _sizes = [(abs(ox-tx) + 1) * (abs(oy-ty) + 1) for ox,oy in _tiles for tx,ty in _tiles]
    return max(_sizes)

# soooo
# I will want to build a "dense map"
# and then do the "stupid is it green" thing
# to do it? gather all coords and arrange them
# build a map
# turn tiles G in the map
# last part is "coloring the loop"?

def flood_fill_matrix(matrix):
    # first row must have "top" which will have . under
    # pick any and flood fill
    for x in range(len(matrix[0])):
        if matrix[0][x] == 'X' and matrix[1][x] == '.':
            seed = (x, 1)
            break

    buffer = [seed]
    while len(buffer) > 0:
        px, py = buffer.pop()
        if matrix[py][px] == '.':
            matrix[py][px] = 'X'
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                if 0 <= px + dx < len(matrix[0]) and 0 <= py + dy < len(matrix):
                    buffer.append((px + dx, py + dy))

    return matrix

def part_two(tiles):
    # Prep - compact the coordinates
    _tiles = [[int(i) for i in tile.split(',')] for tile in tiles]
    _x_coords = [_ for _ in {x[0] for x in _tiles}]
    _y_coords = [_ for _ in {x[1] for x in _tiles}]
    _x_coords.sort()
    _y_coords.sort()

    # Prep 2 - build the map and color it (oof)
    _map = [['.' for _ in range(len(_x_coords))] for __ in range(len(_y_coords))]
    for i in range(len(_tiles)):
        sx, sy = _tiles[i - 1]
        tx, ty = _tiles[i]
        if sy == ty:
            sxi = min(_x_coords.index(sx), _x_coords.index(tx))
            txi = max(_x_coords.index(sx), _x_coords.index(tx))
            yi = _y_coords.index(sy)
            for _x in range(sxi, txi + 1):
                _map[yi][_x] = 'X'
        else:
            syi = min(_y_coords.index(sy), _y_coords.index(ty))
            tyi = max(_y_coords.index(sy), _y_coords.index(ty))
            xi = _x_coords.index(sx)
            for _y in range(syi, tyi + 1):
                _map[_y][xi] = 'X'

    flood_fill_matrix(_map)

    sizes = []
    for ox,oy in _tiles:
        for tx,ty in _tiles:
            oxi = min(_x_coords.index(ox), _x_coords.index(tx))
            txi = max(_x_coords.index(ox), _x_coords.index(tx))
            oyi = min(_y_coords.index(oy), _y_coords.index(ty))
            tyi = max(_y_coords.index(oy), _y_coords.index(ty))
            # if all tiles in the square are X, compute area!
            if all(_map[y][x] == 'X' for y in range(oyi, tyi + 1) for x in range(oxi, txi + 1)):
                sizes.append((abs(tx - ox) + 1) * (abs(ty - oy) + 1))

    return max(sizes)

assert part_one(common.Loader.load_lines('test')) == 50
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test')) == 24
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')