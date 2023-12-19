import common
from colorama import Fore, Back, Style


class PartCrawler:
    def __init__(self, values=None):
        self.values = {}
        if values is None:
            for key in ['s', 'm', 'x', 'a']:
                self.values[key] = (1, 4000)
        else:
            for k, v in values.items():
                self.values[k] = v

    def crawl(self, rule):
        if rule == 'A':
            rv = 1
            for (min, max) in self.values.values():
                rv *= max - min + 1
            return rv
        if rule == 'R':
            return 0
        if rule.operator == '<':
            if self.values[rule.key][1] < rule.value:
                # whole is true
                return self.crawl(rule.true)
            elif self.values[rule.key][0] >= rule.value:
                return self.crawl(rule.false)
            else:
                t = PartCrawler(self.values)
                f = self
                t.values[rule.key] = (t.values[rule.key][0], rule.value - 1)
                f.values[rule.key] = (rule.value, f.values[rule.key][1])
                return t.crawl(rule.true) + f.crawl(rule.false)
        else:
            if self.values[rule.key][0] > rule.value:
                # whole is true
                return self.crawl(rule.true)
            elif self.values[rule.key][1] <= rule.value:
                return self.crawl(rule.false)
            else:
                t = PartCrawler(self.values)
                f = self
                f.values[rule.key] = (f.values[rule.key][0], rule.value)
                t.values[rule.key] = (rule.value + 1, t.values[rule.key][1])
                return t.crawl(rule.true) + f.crawl(rule.false)


class Part:
    def __init__(self, line):
        self.values = {}
        for part in line[1:-1].split(','):
            key, value = part.split('=')
            self.values[key] = int(value)

    def score(self):
        return sum(self.values.values())

    def get_value(self, key):
        return self.values[key] if key in self.values else 0


class Rule:
    def __init__(self, condition):
        if '<' in condition:
            self.operator = '<'
        else:
            self.operator = '>'
        self.key = condition.split(self.operator)[0]
        self.value = int(condition.split(self.operator)[1])
        self.true = None
        self.false = None

    def add_transition(self, rule):
        if self.true is None:
            self.true = rule
        else:
            self.false = rule
            return True
        return False

    def sort(self, part):
        if (self.operator == '<' and part.get_value(self.key) < self.value) or (
                self.operator == '>' and part.get_value(self.key) > self.value):
            if self.true == 'A':
                return True
            if self.true == 'R':
                return False
            return self.true.sort(part)
        else:
            if self.false == 'A':
                return True
            if self.false == 'R':
                return False
            return self.false.sort(part)


def parse_rules(lines):
    in_rule = None
    buffer = []
    rules = {}
    for line in lines:
        key = line.split('{')[0]
        condition, condition_rest = (line.split('{')[1][:-1]).split(':', maxsplit=1)
        r = Rule(condition)
        if line.startswith('in{'):
            in_rule = r
        rules[key] = r
        buffer.append((r, condition_rest))

    for r, condition_rest in buffer:
        parse_one_rule(r, condition_rest, rules)

    # parse rest
    return in_rule


def parse_one_rule(rule, line, rules):
    stack = [rule]
    # if next is , then we have transfer
    while len(line) > 0:
        if ',' not in line and ':' not in line:
            if line in ['A', 'R']:
                if stack[-1].add_transition(line):
                    stack.pop()
            else:
                if stack[-1].add_transition(rules[line]):
                    stack.pop()
            line = ''
        elif (',' in line and ':' in line and line.index(',') < line.index(':')) \
                or (',' in line and ':' not in line):
            # transfer
            t_value, line = line.split(',', maxsplit=1)
            if t_value in ['A', 'R']:
                if stack[-1].add_transition(t_value):
                    stack.pop()
            else:
                if stack[-1].add_transition(rules[t_value]):
                    stack.pop()
        else:
            # condition is next!
            condition, line = line.split(':', maxsplit=1)
            r = Rule(condition)
            if stack[-1].add_transition(r):
                stack.pop()
            stack.append(r)


def solve(lines):
    div = lines.index('')
    in_rule = parse_rules(lines[:div])
    return sum([part.score() for part in [Part(l) for l in lines[div + 1:] if in_rule.sort(Part(l))]])


def get_rating_combinations(lines):
    div = lines.index('')
    in_rule = parse_rules(lines[:div])
    pc = PartCrawler().crawl(in_rule)
    print(pc)
    return pc


assert solve(common.Loader.load_lines('test')) == 19114
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{solve(common.Loader.load_lines())}')

assert get_rating_combinations(common.Loader.load_lines('test')) == 167409079868000
print(f'Part 2: {Back.GREEN}{Fore.BLACK}{get_rating_combinations(common.Loader.load_lines())}')