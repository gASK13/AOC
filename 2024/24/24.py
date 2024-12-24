import common
from colorama import Fore, Style, Back

def run(o1, o2, op):
    if op == 'AND':
        return o1 & o2
    elif op == 'OR':
        return o1 | o2
    elif op == 'XOR':
        return o1 ^ o2
    raise Exception(f'Unknown operation {op}')

def part_one(lines):
    values = {}
    while len(lines[0]) > 0:
        key, val = lines.pop(0).split(': ')
        values[key] = True if val == '1' else False
    lines.pop(0)

    pairs = []
    for line in lines:
        _in, _out = line.split(' -> ')
        o1, op, o2 = _in.split(' ')
        pairs.append((o1,o2,op,_out))

    while len(pairs) > 0:
        unmatched = []
        for o1,o2,op,out in pairs:
            if o1 in values and o2 in values:
                values[out] = run(values[o1], values[o2], op)
            else:
                unmatched.append((o1,o2,op,out))
        if len(pairs) == len(unmatched):
            raise Exception(f'No progress made, unmatched: {unmatched}')
        pairs = unmatched

    i = 0
    ret = 0
    print([f'{v} == {values[v]}' for v in values if v[0] == 'z'])
    for k in sorted([v for v in values if v[0] == 'z'],reverse=True):
        ret *= 2
        ret += 1 if values[k] else 0
        i += 1
    return ret

assert part_one(common.Loader.load_lines('test_4')) == 4
assert part_one(common.Loader.load_lines('test_2024')) == 2024
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

