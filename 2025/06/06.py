import common
from colorama import Fore, Back, Style

def compute_line(hw_line):
    if hw_line[-1] == '*':
        prod = 1
        for i in hw_line[:-1]:
            prod *= int(i)
        return prod
    elif hw_line[-1] == '+':
        return sum([int(i) for i in hw_line[:-1]])
    raise Exception('Not implemented')

def part_one(hw):
    # This expects the "matrix" stripped of whitespaces for simple "tranpose and compute" operation
    hw = common.transpose_matrix(hw)
    return sum([compute_line(line) for line in hw])

def part_two(hw):
    # Expects the full matrix (all chars)
    # Transpose (so the operation is the last column
    # Will break it into sub-matrices by column
    max_len = max([len(i) for i in hw])
    for line in hw:
        line[:] = [item if item != ' ' else '' for item in line]
        line.extend([''] * (max_len - len(line)))
    ops = hw.pop(-1)
    hw = common.transpose_matrix(hw)
    sum = 0
    _cur_op = None
    _cur_num = 0
    for idx, op in enumerate(ops):
        if op == '*' or op == '+':
            sum += _cur_num
            _cur_op = '*' if op == '*' else '+'
            _cur_num = 1 if op == '*' else 0
        if _cur_op == '*':
            _cur_num *= int(''.join(hw[idx])) if ''.join(hw[idx]) != '' else 1
        else:
            _cur_num += int(''.join(hw[idx])) if ''.join(hw[idx]) != '' else 0
    sum += _cur_num
    return sum

assert part_one(common.Loader.load_matrix('test', delimiter='\s+')) == 4277556
data = common.Loader.load_matrix(delimiter="\s+")
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(data)}{Style.RESET_ALL}')

assert part_two(common.Loader.load_matrix('test', strip=False)) == 3263827
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_matrix(strip=False))}{Style.RESET_ALL}')