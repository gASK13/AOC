import common


class Disc:
    def __init__(self, line):
        self.id = int(line.split(' ')[1][1:])
        self.max = int(line.split(' ')[3])
        self.pos = int(line.split(' ')[11][:-1])

    def can_pass(self, start):
        return (start + self.id + self.pos) % self.max == 0


def find_first_time(discs):
    i = 0
    while True:
        if all([d.can_pass(i) for d in discs]):
            return i
        i += 1


def find_second_time(discs):
    discs.append(Disc(f'Disc #{discs[-1].id + 1} has 11 positions; at time=0, it is at position 0.'))
    i = 0
    while True:
        if all([d.can_pass(i) for d in discs]):
            return i
        i += 1


assert find_first_time(common.Loader.transform_lines(Disc, 'tests')) == 5
print(f'Time to fall is {find_first_time(common.Loader.transform_lines(Disc))}')

assert find_second_time(common.Loader.transform_lines(Disc, 'tests')) == 85
print(f'Time to fall is {find_second_time(common.Loader.transform_lines(Disc))}')
