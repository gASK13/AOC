import common


def run_program(start, cycles, lines):
    items = [item for line in lines for item in ([0] if line == 'noop' else [0, int(line.split(' ')[1])])]
    return 1 + sum(items[:cycles - 1])


def solve_first(lines):
    strength = 0
    for cycle in [20, 60, 100, 140, 180, 220]:
        strength += cycle * run_program(1, cycle, lines)
    return strength


def solve_second(lines):
    output = ['', '', '', '', '', '']
    for i in range(6):
        for j in range(40):
            pos = run_program(1, (j+1) + (i*40), lines)
            if pos - 1 <= j <= pos + 1:
                output[i] += '■'
            else:
                output[i] += ' '
    for l in output:
        print(l)


assert run_program(1, 2, ['noop', 'addx 3', 'addx -5']) == 1
assert run_program(1, 3, ['noop', 'addx 3', 'addx -5']) == 1
assert run_program(1, 4, ['noop', 'addx 3', 'addx -5']) == 4
assert run_program(1, 5, ['noop', 'addx 3', 'addx -5']) == 4
assert run_program(1, 6, ['noop', 'addx 3', 'addx -5']) == -1
assert run_program(1, 20, common.Loader.load_lines('test')) == 21
assert run_program(1, 60, common.Loader.load_lines('test')) == 19
assert run_program(1, 100, common.Loader.load_lines('test')) == 18
assert run_program(1, 140, common.Loader.load_lines('test')) == 21
assert run_program(1, 180, common.Loader.load_lines('test')) == 16
assert run_program(1, 220, common.Loader.load_lines('test')) == 18

assert solve_first(common.Loader.load_lines('test')) == 13140
print(f'First part strength is {solve_first(common.Loader.load_lines())}')

solve_second(common.Loader.load_lines('test'))
print('')
print('')
solve_second(common.Loader.load_lines())