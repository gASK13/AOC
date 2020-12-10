import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode import Parostroj


def print_map(_map):
    for line in _map:
        print(''.join([item for item in line]))


def parse_map(_output):
    map = []
    line = []
    for char in _output:
        if char == 10:
            if len(line) > 0:
                map.append(line)
            line = []
        else:
            line.append(chr(char))
    if len(line) > 0:
        map.append(line)
    return map


def count_neighbor_chars(_x, _y, _map, _chars):
    cnt = 0
    for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if (0 <= _x + x < len(_map[0])) & (0 <= _y + y < len(_map)):
            if _map[_y + y][_x + x] in _chars:
                cnt += 1
    return cnt


def align_map(_map):
    sum = 0
    for y in range(1, len(_map) - 1):
        for x in range(1, len(_map[0]) - 1):
            if (_map[y][x] == '#') & (count_neighbor_chars(x, y, _map, ['#']) == 4):
                sum += x*y
    return sum


def find_bot(_map):
    for y in range(1, len(_map) - 1):
        for x in range(1, len(_map[0]) - 1):
            if _map[y][x] in ['^', 'v', '<', '>']:
                return x, y

def turns(_dx, _dy):
    return [(-_dy, _dx, 'R'), (_dy, -_dx, 'L')]

def get_path(_map, _robot):
    path = []
    steps = 0
    _map[_robot[1]][_robot[0]] = 'O'
    while count_neighbor_chars(_robot[0], _robot[1], _map, ['#', 'H']) > 0:
        tx = _robot[0] + _robot[2][0]
        ty = _robot[1] + _robot[2][1]
        if (0 <= tx < len(_map[0])) & (0 <= ty < len(_map)):
            if _map[ty][tx] in ['#', 'H']:
                if count_neighbor_chars(tx, ty, _map, ['#']) <= 1:
                    _map[ty][tx] = 'O'
                else:
                    _map[ty][tx] = 'H'
                steps += 1
                _robot[0] = tx
                _robot[1] = ty
                continue
        if steps > 0:
            path.append(str(steps))
            steps = 0
        for (x, y, dir) in turns(robot[2][0], robot[2][1]):
            if (0 <= _robot[0] + x < len(_map[0])) & (0 <= _robot[1] + y < len(_map)):
                if _map[_robot[1] + y][_robot[0] + x] == '#':
                    _robot[2] = (x, y)
                    path.append(dir)
    if steps > 0:
        path.append(str(steps))
    return path


def replace_in_path(_sub, _subchar, _path):
    new_path = []
    i = 0
    while i < len(_path):
        if _sub == _path[i:i + len(_sub)]:
            new_path.append(_subchar)
            i += len(_sub)
        else:
            new_path.append(_path[i])
            i += 1
    return new_path

def encode(_functions):
    input = []
    for func in _functions:
        for char in ','.join([str(item) for item in func]):
            input.append(ord(char))
        input.append(10)
    input.append(ord('n'))
    input.append(10)
    return input

#map = ['..#..........','..#..........','#######...###', '#.#...#...#.#','#############','..#...#...#..','..#####...^..']
program = open('17.txt', 'r').readline()
map = parse_map(Parostroj(program).run())
print_map(map)

# PART ONE
print(align_map(map))

# PART TWO
bot_pos = find_bot(map)
robot = [bot_pos[0], bot_pos[1], (0, -1)]
path = get_path(map, robot)
print(path)
print(len(path))

# hand crafted to perfection !!
a = ['L', '12', 'L', '8', 'R', '12']
b = ['L', '10', 'L', '8', 'L', '12', 'R', '12']
c = ['R', '12', 'L', '8', 'L', '10']
path = replace_in_path(a, 'A', path)
path = replace_in_path(b, 'B', path)
path = replace_in_path(c, 'C', path)
print(path)
print(len(path))
print(encode([path, a, b, c]))

program_clean = '2' + program[1:]
#Parostroj(program_clean, output_processor=lambda x:print(chr(x), end='')).run(input_array=encode([path, a, b, c]))
out = Parostroj(program_clean).run(input_array=encode([path, a, b, c]))
print(out[-1])
