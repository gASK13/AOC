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

def find_solutions(goal, iterations=4):
    results = {goal}
    for i in range(iterations - 1):
        print(f'Iteration {i} has {len(results)} results at start...')
        results2 = set()
        for r in results: #second robot
            results2.update(use_keypad(r))
        smin = min([len(s) for s in results2])
        results = set([r for r in results2 if len(r) == smin])
    return results

def part_one(lines):
    retval = 0
    for l in lines:
        num = int(l[:-1])
        sols = find_solutions(l)
        smin = min([len(s) for s in sols])
        retval += smin * num
    return retval

def part_two(lines):
    retval = 0
    for l in lines:
        num = int(l[:-1])
        sols = find_solutions(l, 27)
        smin = min([len(s) for s in sols])
        retval += smin * num
    return retval

assert '<vA<AA>>^AvAA<^A>Av<<A>>^AvA^A<vA>^Av<<A>^A>AAvA^Av<<A>A>^AAAvA<^A>A' in find_solutions('029A')
assert part_one(['029A']) == 68*29
assert part_one(['980A']) == 60*980
assert part_one(['179A']) == 68*179
assert part_one(['456A']) == 64*456
assert part_one(['379A']) == 64*379
assert part_one(['029A', '980A','179A','456A','379A']) == 126384

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

# part 2 is 27 iterations (!!!)

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')