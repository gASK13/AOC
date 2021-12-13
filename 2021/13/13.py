import common


class Matrix:
    def __init__(self, lines):
        self.matrix = set()
        for line in lines:
            x = int(line.split(',')[0])
            y = int(line.split(',')[1])
            self.matrix.add((x, y))

    def fold(self, line):
        val = int(line.split('=')[1])
        if line.split('=')[0] == 'fold along y':
            flip = [(x, val - (y - val)) for x, y in self.matrix if y > val]
            self.matrix = set([(x, y) for x, y in self.matrix if y < val] + flip)
        else:
            flip = [(val - (x - val), y) for x, y in self.matrix if x > val]
            self.matrix = set([(x, y) for x, y in self.matrix if x < val] + flip)

    def dot_count(self):
        return len(self.matrix)

    def print(self):
        print('\n'.join(
            [''.join(['#' if (i, j) in self.matrix else ' ' for i in range(1 + max([x for x, y in self.matrix]))])
             for j in range(1 + max([y for x, y in self.matrix]))]))


def run(lines):
    data = lines[:lines.index('')]
    instructions = lines[lines.index('') + 1:]
    m = Matrix(data)
    for line in instructions:
        m.fold(line)
        if line == instructions[0]:
            print(f'First fold is {m.dot_count()}')
    return m


run(common.Loader.load_lines("test.txt"))
m = run(common.Loader.load_lines())
m.print()

# 18->17->16
