import common
from colorama import Fore,Back,Style

def get_all_move_combos(x,y,zx,zy,none_corner):
    x_part = ''.join(['<' if zx < x else '>' for _ in range(abs(zx-x))])
    y_part = ''.join(['^' if zy < y else 'v' for _ in range(abs(zy-y))])
    # avoid combos over certain corner!
    if x == none_corner[0] and zy == none_corner[1]:
        return {x_part + y_part}
    if zx == none_corner[0] and y == none_corner[1]:
        return {y_part + x_part}
    return {x_part + y_part, y_part + x_part}

def generate_transitions():
    matrices = [([['7','8','9'], ['4','5','6'], ['1','2','3'], [None, '0', 'A']], (0,3)),
                ([[None, '^', 'A'],['<','v','>']], (0,0))]
    transitions = {}
    for matrix, none_corner in matrices:
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x] is None:
                    continue
                if matrix[y][x] not in transitions:
                    transitions[matrix[y][x]] = {}
                for zy in range(len(matrix)):
                    for zx in range(len(matrix[0])):
                        if matrix[zy][zx] is None or (zx == x and zy == y):
                            continue
                        if matrix[zy][zx] not in transitions[matrix[y][x]]:
                            transitions[matrix[y][x]][matrix[zy][zx]] = set()
                        transitions[matrix[y][x]][matrix[zy][zx]].update(get_all_move_combos(x, y, zx, zy, none_corner))
    return transitions

_TRANSITIONS = generate_transitions()

def use_keypad(goal):
    position = 'A'
    results = ['']
    for c in goal:
        if c == position:
            results = [r+'A' for r in results]
        else:
            results = [r+t+'A' for r in results for t in _TRANSITIONS[position][c]]
            position = c
    return results

def find_solutions(goal, iterations=2):
    moves = {'A', '<A', 'vA', '>A', '^A', '<<A', 'vvA', '>>A', '^^A', '<vA', '<^A', '>vA', '>^A', 'v<A', 'v>A', '^<A', '^>A',
                    '<<vA', '<<^A', 'vv<A', 'vv>A', '>>vA', '>>^A', '^^<A', '^^>A',
                    'v<<A', '^<<A', '<vvA', '>vvA', 'v>>A', '^>>A', '<^^A', '>^^A',
                    '<<^^A', '<<vvA', 'vv<<A', 'vv>>A', '>>^^A', '>>vvA', '^^<<A', '^^>>A',
                    '^^^A', '^^^<A', '^^^<<A','^^^>A',
                    '<^^^A','>^^^A',
                    'vvvA', 'vvv<A','vvv>A','<vvvA', '>>vvvA'}

    # original needs to be 2 steps!
    lengths = {}
    for key in moves:
        lengths[key] = len(key)
    for key in moves:
        lengths[key] = min([len(ir) for r in use_keypad(key) for ir in use_keypad(r)])

    for i in range(iterations-2):
        new_lengths = {}
        for key in moves:
            new_lengths[key] = 999999999999
            for r in use_keypad(key):
                # break after each A, but keep the A as part of string
                buff = ''
                ln = 0
                for c in r:
                    if c == 'A':
                        ln += lengths[buff+c]
                        buff = ''
                    else:
                        buff += c
                assert buff == '' #should not end by anything then A
                if ln < new_lengths[key]:
                    new_lengths[key] = ln
        lengths = new_lengths

    smin = 999999999999
    for r in use_keypad(goal):
        # break after each A, but keep the A as part of string
        buff = ''
        ln = 0
        for c in r:
            if c == 'A':
                ln += lengths[buff + c]
                buff = ''
            else:
                buff += c
        assert buff == ''  # should not end by anything then A
        if ln < smin:
            smin = ln
    print(smin)
    return smin

def part_one(lines):
    retval = 0
    for l in lines:
        num = int(l[:-1])
        smin = find_solutions(l)
        retval += smin * num
    return retval

def part_two(lines):
    retval = 0
    for l in lines:
        num = int(l[:-1])
        smin = find_solutions(l, 25)
        retval += smin * num
    return retval

assert part_one(['029A']) == 68*29
assert part_one(['980A']) == 60*980
assert part_one(['179A']) == 68*179
assert part_one(['456A']) == 64*456
assert part_one(['379A']) == 64*379
assert part_one(['029A', '980A','179A','456A','379A']) == 126384

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

# part 2 is 27 iterations (!!!)

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')


# Any "switch" will result in a "move" which will always have the same smallest signature in the end
# it is bound to repeat?