from numpy.f2py.auxfuncs import isint1

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

class Node:
    def __init__(self, name):
        self._name = name

    def eval(self):
        pass

class Constant(Node):
    def __init__(self, name, value):
        super().__init__(name)
        self._value = value

    def eval(self):
        return self._value

    def __eq__(self, other):
        if not isinstance(other, Constant):
            return False
        return self._name == other._name

    def __lt__(self, other):
        if not isinstance(other, Constant):
            return False
        return self._name < other._name

    def __str__(self):
        return f'{self._name}'

    def __repr__(self):
        return f'{self._name}'

class LogicTree(Node):
    def __init__(self, name, o1, o2, op):
        super().__init__(name)
        self._o1 = min(o1,o2)
        self._o2 = max(o1,o2)
        self._op = op

    def eval(self):
        return run(self._o1.eval(), self._o2.eval(), self._op)

    def __eq__(self, other):
        if not isinstance(other, LogicTree):
            return False
        return self._o1 == other._o1 and self._o2 == other._o2 and self._op == other._op

    def __lt__(self, other):
        if not isinstance(other, LogicTree):
            return True
        if self._op != other._op:
            return self._op < other._op
        if self._o1 != other._o1:
            return self._o1 < other._o1
        return self._o2 < other._o2

    def __str__(self):
        return f'[{self._o1} {self._op} {self._o2}]'

    def __repr__(self):
        return f'[{self._o1} {self._op} {self._o2}]'

    def diff(self, other):
        if self == other:
            return None
        # Diff can be > op is different but o1/o2 are same
        # o1 is different but o2 is same (and op)
        # o2 is different but o1 is same (and op)
        if self._op != other._op:
            if self._o1 == other._o1 and self._o2 == other._o2:
                return f'{self._name}/{other._name} op is different {self._op} vs {other._op}'
            else:
                return f'{self._name}/{other._name} are totally different {self} vs {other}'
        elif self._o1 != other._o1:
            if isinstance(self._o1, LogicTree) and isinstance(other._o1, LogicTree):
                return self._o1.diff(other._o1)
            else:
                return f'{self._name}/{other._name} o1 is different {self._o1} vs {other._o1}'
        else:
            if isinstance(self._o2, LogicTree) and isinstance(other._o2, LogicTree):
                return self._o2.diff(other._o2)
            else:
                return f'{self._name}/{other._name} o2 is different {self._o2} vs {other._o2}'






def part_one(lines):
    values = parse_lines(lines)

    i = 0
    ret = 0
    for k in sorted([v for v in values if v[0] == 'z'],reverse=True):
        ret *= 2
        ret += 1 if values[k].eval() else 0
        i += 1
    return ret


def parse_lines(lines, subs=[]):
    _subs = {}
    for s1, s2 in subs:
        _subs[s1] = s2
        _subs[s2] = s1

    values = {}
    while len(lines[0]) > 0:
        key, val = lines.pop(0).split(': ')
        values[key] = Constant(key, True if val == '1' else False)
    lines.pop(0)
    while len(lines) > 0:
        line = lines.pop(0)
        _in, _out = line.split(' -> ')
        if _out in _subs:
            _out = _subs[_out]
        o1, op, o2 = _in.split(' ')
        if o1 in values and o2 in values:
            values[_out] = LogicTree(_out, values[o1], values[o2], op)
        else:
            lines.append(line)
    return values

def find_matching_node(node, values):
    for k in values:
        if node == values[k]:
            return values[k]
    return None

def find_match(start, values, k):
    if find_matching_node(start, values) is not None:
        print(f'{k} should be {find_matching_node(start, values)._name}')
    else:
        # same op and one half?
        if start._op == values[k]._op:
            if start._o1 == values[k]._o1:
                if find_matching_node(start._o2, values) is not None:
                    print(f'{values[k]._o2._name} should be {find_matching_node(start._o2, values)._name}')
                else:
                    find_match(start._o2, values, values[k]._o2._name)
            elif start._o1 == values[k]._o2:
                if find_matching_node(start._o2, values) is not None:
                    print(f'{values[k]._o1._name} should be {find_matching_node(start._o2, values)._name}')
                else:
                    find_match(start._o2, values, values[k]._o1._name)
            elif start._o2 == values[k]._o2:
                if find_matching_node(start._o1, values) is not None:
                    print(f'{values[k]._o1._name} should be {find_matching_node(start._o1, values)._name}')
                else:
                    find_match(start._o1, values, values[k]._o1._name)
            elif start._o2 == values[k]._o1:
                if find_matching_node(start._o1, values) is not None:
                    print(f'{values[k]._o2._name} should be {find_matching_node(start._o1, values)._name}')
                else:
                    find_match(start._o1, values, values[k]._o2._name)
            else:
                print(f'{k} has same OP but both sides different!!!')
        else:
            print(f'{k} has different OP!!!')

def part_two(lines):
    # Gathered via DEBUG manually
    values = parse_lines(lines, [['z10', 'mkk'],['z14', 'qbw'], ['z34', 'wcb'], ['cvp','wjb']])

    idx = 0
    start = find_matching_node(LogicTree('START', values[f'x{idx:02d}'], values[f'y{idx:02d}'], 'XOR'), values)
    assert start is not None
    print(sorted([v for v in values if v[0] == 'x']))
    for k in sorted([v for v in values if v[0] == 'z']):
        # valid pair is 0 XOR 0
        if start != values[k]:
            find_match(start, values, k)

        new_s = find_matching_node(LogicTree('START', start._o1, start._o2, 'AND'), values)
        assert new_s is not None
        start = new_s
        if len([v for v in values if v[0] == 'x']) > idx > 0:
            tmp = find_matching_node(LogicTree('START', values[f'x{idx:02d}'],  values[f'y{idx:02d}'], 'AND'), values)
            assert tmp is not None
            new_s = find_matching_node(LogicTree('START', start, tmp,  'OR'), values)
            assert new_s is not None
            start = new_s
        idx += 1
        if idx < len([v for v in values if v[0] == 'x']):
            tmp = find_matching_node(LogicTree('START', values[f'x{idx:02d}'], values[f'y{idx:02d}'], 'XOR'), values)
            assert tmp is not None
            new_s = find_matching_node(LogicTree('START', tmp, start, 'XOR'), values)
            assert new_s is not None
            start = new_s

        # The code should try to "build" the tree using existing bricks and then see if it matches next brick on all parts
        # This is more steps
        # - one is the "prev with AND" part
        # - one is the "N-1 AND N-1" part
        # - one is the OR of previous t wo
        # - one is the "N XOR N" constant part
        # - last one is the XOR of previous two

        # then [1 XOR 1] XOR [prev with AND]
        # then [2 XOR 2] XOR [[prev with AND] OR 1 AND 1]
        # then [3 XOR 3] XOR [[prev with AND] OR 2 AND 2]


assert part_one(common.Loader.load_lines('test_4')) == 4
assert part_one(common.Loader.load_lines('test_2024')) == 2024
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')


