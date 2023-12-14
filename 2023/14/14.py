import common
from colorama import Fore, Back, Style

class Platform:
    def __init__(self, lines):
        self.platform = [[c for c in line] for line in lines]

    def tilt_north(self):
        for i in range(len(self.platform)):
            for j in range(len(self.platform[0])):
                if self.platform[i][j] == 'O':
                    di = i
                    while di > 0 and self.platform[di-1][j] == '.':
                        di -= 1
                    self.platform[i][j] = '.'
                    self.platform[di][j] = 'O'

    def cycle(self, num=1):
        # tilt N, W, S, E
        seen = {}
        seen_order = []
        for _ in range(num):
            if str(self) in seen:
                idx = seen[str(self)]
                cycle = _ - idx
                print(f'Cycle of {cycle} found at {_}')
                print(f'Load at {(num - idx) % cycle + idx}: {seen_order[(num - idx) % cycle + idx]}')
                return seen_order[(num - idx) % cycle + idx]
            seen[str(self)] = _
            seen_order.append(self.get_load())
            for i in range(4):
                self.tilt_north()
                self.platform = common.rotate_matrix_cw(self.platform)
        return self.get_load()

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.platform])

    def __repr__(self):
        return self.__str__()

    def get_load(self):
        return sum([sum([len(self.platform) - i for _ in line if _ == 'O']) for i,line in enumerate(self.platform)])


def load_after_tilt(platform):
    platform.tilt_north()
    return platform.get_load()


assert load_after_tilt(Platform(common.Loader.load_lines('test'))) == 136

print(f'Part 1: {Back.GREEN}{Fore.BLACK}{load_after_tilt(Platform(common.Loader.load_lines()))}')

assert Platform(common.Loader.load_lines('test')).cycle(1000000000) == 64

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{Platform(common.Loader.load_lines()).cycle(1000000000)}')
