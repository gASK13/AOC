import common
from colorama import Fore, Back, Style
import tqdm


def decode_hexa(hexa):
    direction = None
    match hexa[-1]:
        case '0':
            direction = 'R'
        case '1':
            direction = 'D'
        case '2':
            direction = 'L'
        case '3':
            direction = 'U'

    return direction, int(hexa[1:-1], 16)

def get_compressions(lines, decode=False):
    # get list of "ranges" that we can use (break points)
    v_compression = {0}
    h_compression = {0}
    pos = (0, 0)
    for line in lines:
        if decode:
            direction, length = decode_hexa(line.split('(')[1][:-1])
        else:
            length = int(line.split(' ')[1])
            direction = line[0]
        match direction:
            case 'D':
                v_compression.add(pos[1] + length)
                pos = (pos[0], pos[1] + length)
            case 'U':
                v_compression.add(pos[1] - length)
                pos = (pos[0], pos[1] - length)
            case 'R':
                h_compression.add(pos[0] + length)
                pos = (pos[0] + length, pos[1])
            case 'L':
                h_compression.add(pos[0] - length)
                pos = (pos[0] - length, pos[1])

    return convert_to_ranges(list(h_compression)), convert_to_ranges(list(v_compression))


def convert_to_ranges(compression):
    compression.sort()
    # now transform this into "lines" and "ranges"
    final = [compression[0]]
    for i in range(len(compression) - 1):
        if compression[i + 1] - compression[i] > 1:
            final.append((compression[i] + 1, compression[i + 1]))
        final.append(compression[i + 1])
    return final


def solve(lines, decode=False):
    # so what I would like to do is store "compressed" coordinates which will be broken down when new ones are entered
    h_compression, v_compression = get_compressions(lines, decode)

    # find index of 0 and start there
    pos = (h_compression.index(0), v_compression.index(0))
    edges = [pos]

    for line in lines:
        if decode:
            direction, length = decode_hexa(line.split('(')[1][:-1])
        else:
            length = int(line.split(' ')[1])
            direction = line[0]
        match direction:
            case 'D':
                new_y = v_compression.index(v_compression[pos[1]] + length)
                for i in range(new_y - pos[1]):
                    edges.append((pos[0], pos[1] + i + 1))
                pos = (pos[0], new_y)
            case 'U':
                new_y = v_compression.index(v_compression[pos[1]] - length)
                for i in range(pos[1] - new_y):
                    edges.append((pos[0], pos[1] - i - 1))
                pos = (pos[0], new_y)
            case 'R':
                new_x = h_compression.index(h_compression[pos[0]] + length)
                for i in range(new_x - pos[0]):
                    edges.append((pos[0] + i + 1, pos[1]))
                pos = (new_x, pos[1])
            case 'L':
                new_x = h_compression.index(h_compression[pos[0]] - length)
                for i in range(pos[0] - new_x):
                    edges.append((pos[0] - i - 1, pos[1]))
                pos = (new_x, pos[1])

    matrix = [['.' for _ in range(len(h_compression))] for _ in range(len(v_compression))]
    for x, y in edges:
        matrix[y][x] = '#'

    flood_fill_matrix(matrix)

    # now count - this is going to be a bit ... tricky
    total = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == '#':
                v_factor = 1 if isinstance(v_compression[y], int) else v_compression[y][1] - v_compression[y][0]
                h_factor = 1 if isinstance(h_compression[x], int) else h_compression[x][1] - h_compression[x][0]
                total += v_factor * h_factor
    # now return count
    return total


def flood_fill_matrix(matrix):
    # first row must have "top" which will have . under
    # pick any and flood fill
    for x in range(len(matrix[0])):
        if matrix[0][x] == '#' and matrix[1][x] == '.':
            seed = (x, 1)
            break

    buffer = [seed]
    while len(buffer) > 0:
        px, py = buffer.pop()
        if matrix[py][px] == '.':
            matrix[py][px] = '#'
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                if 0 <= px + dx < len(matrix[0]) and 0 <= py + dy < len(matrix):
                    buffer.append((px + dx, py + dy))

    return matrix


assert solve(common.Loader.load_lines('test')) == 62

print(f'Part 1: {Back.GREEN}{Fore.BLACK}{solve(common.Loader.load_lines())}')

assert solve(common.Loader.load_lines('test'), True) == 952408144115

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{solve(common.Loader.load_lines(), True)}')