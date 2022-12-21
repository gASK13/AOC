import common


class Formula:
    def __init__(self, line):
        self.key = line.split(':')[0]
        self._formula = None
        self.formula = line.split(': ')[1]
        self.needed = []
        self._needed = []
        if not self.formula.isnumeric():
            self.needed = self.formula.split(' ')[::2]
        self.expected = 0

    def replace(self, dict):
        new_need = []
        for f in self._needed:
            if f in dict:
                self._formula = self._formula.replace(f, f'({dict[f].formula})')
                new_need += dict[f].needed
            else:
                new_need += [f]
        self._needed = new_need
        return len(self._needed) > 0

    def solve(self, dict):
        self._formula = self.formula
        self._needed = [n for n in self.needed]
        while self.replace(dict):
            if self._needed == ['humn']:
                return None
        return int(eval(self._formula))


def find_root(formulas):
    dict = {}
    for f in formulas:
        dict[f.key] = f
    return dict['root'].solve(dict)

def find_root_humn(formulas):
    dict = {}
    for f in formulas:
        dict[f.key] = f
    # For left and right
    # if it can be solved, solve and take number
    # then take other and "reverse engineer" it recursively
    del dict['humn']  # this is ME
    curr = dict['root']
    if dict[curr.needed[0]].solve(dict) is None:
        curr.needed.reverse()
    val = dict[curr.needed[0]].solve(dict)
    curr = dict[curr.needed[1]]
    curr.expected = val
    while True:
        if curr.needed[0] == 'humn' or dict[curr.needed[0]].solve(dict) is None:
            val = dict[curr.needed[1]].solve(dict)
            ne = curr.expected
            match curr.formula.split(' ')[1]:
                case '*':
                    ne /= val
                case '-':
                    ne += val
                case '/':
                    ne *= val
                case '+':
                    ne -= val
            if curr.needed[0] == 'humn':
                return int(ne)
            curr = dict[curr.needed[0]]
            curr.expected = ne
        else:
            val = dict[curr.needed[0]].solve(dict)
            ne = curr.expected
            match curr.formula.split(' ')[1]:
                case '*':
                    ne /= val
                case '-':
                    ne = val - ne
                case '/':
                    ne = val / ne
                case '+':
                    ne -= val
            if curr.needed[1] == 'humn':
                return int(ne)
            curr = dict[curr.needed[1]]
            curr.expected = ne


assert find_root(common.Loader.transform_lines(Formula, 'test')) == 152
print(f'Root is: {find_root(common.Loader.transform_lines(Formula))}')


assert find_root_humn(common.Loader.transform_lines(Formula, 'test')) == 301
print(f'HUMN root is: {find_root_humn(common.Loader.transform_lines(Formula))}')


#humn = xxx
#root == equals
#301