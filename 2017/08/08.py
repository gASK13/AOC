import common


class CodeLine:
    def __init__(self, line):
        split = line.split(' ')
        self.condition = split[4]
        self.output = split[0]
        self.operation = '{} if {} else 0'.format(
            '{}{}'.format('-' if split[1] == 'dec' else '', split[2]),
            line.split(' if ')[1])

    def apply(self, _vars):
        for x in {self.condition, self.output}:
            if x not in _vars:
                _vars[x] = 0
        _vars[self.output] += eval(self.operation, _vars.copy())

    def __str__(self):
        return '{} = {}'.format(self.output, self.operation)


code = common.Loader.transform_lines(CodeLine)
#code = common.Loader.transform_lines(CodeLine, 'text.txt')
registers = {}
max_val = 0
for c in code:
    c.apply(registers)
    max_val = max([registers[x] for x in registers] + [max_val])

print(max([registers[x] for x in registers]))
print(max_val)
