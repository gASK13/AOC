import common


class Rule:
    def __init__(self, line):
        self.__rule = line
        rule_input = line.split(' => ')[0].split('/')
        rule_output = line.split(' => ')[1].split('/')
        if len(rule_output) == 3:
            self.__raw_outputs = ['/'.join(rule_output)]
        else:
            self.__raw_outputs = [rule_output[x*2][y*2:y*2+2] + '/' + rule_output[x*2 + 1][y*2:y*2+2]
                                  for x in range(2) for y in range(2)]
        # flip
        self.__patterns = ['/'.join(rule_input), '/'.join(reversed(rule_input))]
        # rotate 90
        self.__patterns += ['/'.join([''.join(line) for line in list(zip(*p.split('/')[::-1]))]) for p in self.__patterns]
        # rotate 180
        self.__patterns += ['/'.join([''.join(reversed(l)) for l in reversed(p.split('/'))]) for p in self.__patterns]

        self.__outputs = None

    def join_outputs(self, rules):
        self.__outputs = {}
        for output in self.__raw_outputs:
            for rule in rules:
                if rule.matches(output):
                    if rule not in self.__outputs:
                        self.__outputs[rule] = 0
                    self.__outputs[rule] += 1

    def matches(self, pattern):
        return pattern in self.__patterns

    def run(self, iterations):
        # output is "patter" : count
        if iterations == 1:
            retval = {}
            for raw_output in self.__raw_outputs:
                if raw_output not in retval:
                    retval[raw_output] = 0
                retval[raw_output] += 1
            print(f'Rule {self.__rule} -> RAW output size {sum(retval.values())}')
            return retval
        else:
            retval = {}
            for subrule in self.__outputs:
                suboutput = subrule.run(iterations - 1)
                for raw_output in suboutput:
                    if raw_output not in retval:
                        retval[raw_output] = 0
                    retval[raw_output] += suboutput[raw_output] * self.__outputs[subrule]
            print(f'Rule {self.__rule} @ {iterations} -> output size {sum(retval.values())}')
            return retval

    def __key(self):
        return self.__rule

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Rule):
            return self.__key() == other.__key()
        return NotImplemented


def run_program(patterns=None, iterations=2):
    start_pattern = '.#./..#/###'
    if patterns is None:
        patterns = common.Loader.load_lines()
    rules = [Rule(line) for line in patterns]
    for r in rules:
        r.join_outputs(rules)
    for r in rules:
        if r.matches(start_pattern):
            output = r.run(iterations)
            print(output)
            return sum([s.count('#') * output[s] for s in output])


test_rules = ['../.# => ##./#../...', '.#./..#/### => #..#/..../..../#..#']
assert run_program(test_rules, 2) == 12

print(run_program(iterations=5))

# 3-> 4-> 6-> 8-> 12-> 16
# 16x16 is 8x8 is 64, which is ... not the case
# 34

#106 is ... too low???








