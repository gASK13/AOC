import common


class Monkey:
    def __init__(self, lines):
        self.id = int(lines.pop(0).split(' ')[1][:-1])
        self.items = [int(i) for i in lines.pop(0).split(': ')[1].split(', ')]
        self.operation = lines.pop(0).split('= ')[1]
        self.divisible = int(lines.pop(0).split(' ')[-1])
        self.true = int(lines.pop(0).split(' ')[-1])
        self.false = int(lines.pop(0).split(' ')[-1])
        self.inspects = 0

    def link_monkey(self, monkeys):
        self.true = monkeys[self.true]
        self.false = monkeys[self.false]

    def do_operation(self, old):
        if '*' in self.operation:
            new = 1
            for op in self.operation.split(' * '):
                if op == 'old':
                    new *= old
                else:
                    new *= int(op)
            return new
        elif '+' in self.operation:
            new = 0
            for op in self.operation.split(' + '):
                if op == 'old':
                    new += old
                else:
                    new += int(op)
            return new

    def take_turn(self, divisor = None):
        while len(self.items) > 0:
            self.inspects += 1
            item = self.items.pop(0)
            item = self.do_operation(item)
            if divisor is None:
                item = item // 3
            else:
                item %= divisor
            self.true.items.append(item) if item % self.divisible == 0 else self.false.items.append(item)


def load_monkeys(filename=None):
    _monkeys = common.Loader.transform_lines_complex(Monkey, filename=filename)
    for _m in _monkeys:
        _m.link_monkey(_monkeys)
    return _monkeys


def run_turns(_monkeys, turns, divisor=None):
    for i in range(turns):
        for _m in _monkeys:
            _m.take_turn(divisor)
    score = [m.inspects for m in _monkeys]
    score.sort()
    return score


def get_divisor(_monkeys):
    divisor = 1
    for i in list(set([m.divisible for m in _monkeys])):
        divisor *= i
    return divisor


# TEST PHASE
assert run_turns(load_monkeys('test'), 20) == [7, 95, 101, 105]
assert run_turns(load_monkeys('test'), 1000, get_divisor(load_monkeys('test'))) == [199, 4792, 5192, 5204]
assert run_turns(load_monkeys('test'), 10000, get_divisor(load_monkeys('test'))) == [1938, 47830, 52013, 52166]


# REAL PART ONE
monkeys = load_monkeys()
score = run_turns(monkeys, 20)
print(f'Part one monkey business is :{score[-1] * score[-2]}')

monkeys = load_monkeys()
score = run_turns(monkeys, 10000, get_divisor(monkeys))
print(f'Part two monkey business is :{score[-1] * score[-2]}')

