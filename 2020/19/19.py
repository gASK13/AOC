import re


class Rule:
    def __init__(self, _line):
        self.number = int(_line.split(':')[0])
        self.rule = Rule.parse_rule(_line.split(': ')[1])
        self.final_rule = None
        if re.match('"[a-z]"', self.rule):
            self.final_rule = self.rule[1]
        self.apply_rule_11_placeholder()

    def apply_rule_11_placeholder(self):
        if self.number == 11:
            self.rule = self.rule.replace('><', '>@<')

    def __str__(self):
        return self.rule

    def __repr__(self):
        return self.rule

    def apply(self, _rule):
        if self.final_rule is not None:
            return False

        self.rule = self.rule.replace('<{}>'.format(_rule.number), _rule.final_rule)
        if re.fullmatch('[a-z|()@+?:]*', self.rule):
            if self.number == 8:
                self.final_rule = '(?:{})+'.format(self.rule)
            else:
                self.final_rule = self.rule
            return True
        return False

    @staticmethod
    def parse_rule(_rule):
        if '|' in _rule:
            return'(?:{})'.format('|'.join([Rule.parse_rule(x) for x in _rule.split(' | ')]))
        elif '"' in _rule:
            return _rule
        else:
            return ''.join(['<{}>'.format(x) for x in _rule.split(' ')])


rules = {}
messages = []
read_mode = 'rules'
for line in open('19.txt', 'r').readlines():
    line = line.strip()
    if len(line) == 0:
        read_mode = 'messages'
    elif read_mode == 'rules':
        rule = Rule(line)
        rules[rule.number] = rule
    else:
        messages.append(line)

stack = []
for rule in rules.values():
    if rule.final_rule is not None:
        stack.append(rule)

while len(stack) > 0:
    final = stack.pop(0)
    for rule in rules.values():
        if rule.apply(final):
            stack.append(rule)

patterns = []
base = rules[0].final_rule
# I tried approach via replace, capture groups and whatnot
# in the end I just ended up with about a dozen recursively generated patterns I used on each message
for i in range(0, 10):
    patterns.append(re.compile(base.replace('@', '')))
    base = base.replace('@', rules[11].final_rule)

cnt = 0
for message in messages:
    if any([pattern.fullmatch(message) for pattern in patterns]):
        cnt += 1

print(cnt)






