import common


class Rule:
    def __init__(self, line):
        self.__rule = line
        rule_input = line.split(' => ')[0].split('/')
        self.output = line.split(' => ')[1].split('/')

        # flip
        self.patterns = ['/'.join(rule_input), '/'.join(reversed(rule_input))]
        # rotate 90
        self.patterns += ['/'.join([''.join(line) for line in list(zip(*p.split('/')[::-1]))]) for p in self.patterns]
        # rotate 180
        self.patterns += ['/'.join([''.join(reversed(l)) for l in reversed(p.split('/'))]) for p in self.patterns]

    def __key(self):
        return self.__rule

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Rule):
            return self.__key() == other.__key()
        return NotImplemented


def run_program(patterns=None, iterations=2):
    pattern = '.#./..#/###'.split('/')
    rules = common.Loader.transform_lines(Rule) if patterns is None else [Rule(line) for line in patterns]
    rule_map = {}
    for r in rules:
        for p in r.patterns:
            rule_map[p] = r.output

    for i in range(iterations):
        size = len(pattern)
        if size % 2 == 0:
            output = [['' for a in range(size // 2 * 3)] for b in range(size // 2 * 3)]
            for y in range(size // 2):
                for x in range(size // 2):
                    replacement = rule_map[pattern[y*2][x*2:x*2+2] + '/' + pattern[y*2 + 1][x*2:x*2+2]]
                    for dy in range(3):
                        for dx in range(3):
                            output[y*3 + dy][x*3 + dx] = replacement[dy][dx]
        else:
            output = [['' for a in range(size // 3 * 4)] for b in range(size // 3 * 4)]
            for y in range(size // 3):
                for x in range(size // 3):
                    replacement = rule_map[pattern[y * 3][x * 3:x * 3 + 3]
                                           + '/' + pattern[y * 3 + 1][x * 3:x * 3 + 3]
                                           + '/' + pattern[y * 3 + 2][x * 3:x * 3 + 3]]
                    for dy in range(4):
                        for dx in range(4):
                            output[y * 4 + dy][x * 4 + dx] = replacement[dy][dx]
        pattern = [''.join(p) for p in output]
    return sum([p.count('#') for p in pattern])


test_rules = ['../.# => ##./#../...', '.#./..#/### => #..#/..../..../#..#']
assert run_program(test_rules, 2) == 12

print(run_program(iterations=5))
print(run_program(iterations=18))







