import common


class Warehouse:
    def __init__(self, lines):
        line = lines.pop(0)
        self._stacks = [[] for i in range((len(line) + 1) // 4)]
        while line != '':
            while ((len(line) + 1) // 4) > len(self._stacks):
                self._stacks.append([])
            for i in range(len(self._stacks)):
                if line[i*4] == '[':
                    self._stacks[i].insert(0, line[i*4+1])
            line = lines.pop(0)
        self._instructions = lines

    def run_step(self, new=False):
        if len(self._instructions) == 0:
            return False
        instruction = self._instructions.pop(0).split(' ')
        count = int(instruction[1])
        frm = int(instruction[3]) - 1
        to = int(instruction[5]) - 1
        if new:
            self._stacks[to] += self._stacks[frm][-count:]
            for i in range(count):
                self._stacks[frm].pop()
        else:
            for i in range(count):
                self._stacks[to].append(self._stacks[frm].pop())
        return True

    def __str__(self):
        return '\n'.join([f'{i+1}: {self._stacks[i]}' for i in range(len(self._stacks))])

    def __repr__(self):
        return str(self)

    def message(self, new=False):
        while True:
            if not self.run_step(new):
                break
        return ''.join([c[-1] for c in self._stacks])


assert common.Loader.transform_lines_complex(Warehouse, filename='test.txt', limit=None, strip=False)[0].message() == 'CMZ'
print(f'Message is {common.Loader.transform_lines_complex(Warehouse, limit=None, strip=False)[0].message()}')

assert common.Loader.transform_lines_complex(Warehouse, filename='test.txt', limit=None, strip=False)[0].message(True) == 'MCD'
print(f'Message for 9001 is {common.Loader.transform_lines_complex(Warehouse, limit=None, strip=False)[0].message(True)}')


