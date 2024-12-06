import common
from colorama import Fore, Back

DIRECTIONS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
ORDER = ['^', '>', 'v', '<']

class Guard:
    def __init__(self, _map):
        self.map = _map
        for idy, line in enumerate(_map):
            if '^' in line:
                self.x = line.index('^')
                self.y = idy
                break

    def patrol(self):
        while self.step():
            pass

        return sum([line.count('X') for line in self.map])

    def step(self):
        dx, dy = DIRECTIONS[self.map[self.y][self.x]]
        if self.x + dx < 0 or self.y + dy < 0 or self.x + dx >= len(self.map[0]) or self.y + dy >= len(self.map):
            self.map[self.y][self.x] = 'X'
            return False
        if self.map[self.y + dy][self.x + dx] == '#':
            self.map[self.y][self.x] = ORDER[(ORDER.index(self.map[self.y][self.x]) + 1) % len(ORDER)]
        else:
            self.x += dx
            self.y += dy
            self.map[self.y][self.x] = self.map[self.y - dy][self.x - dx]
            self.map[self.y - dy][self.x - dx] = 'X'
        return True


    def __str__(self):
        return '\n'.join([''.join(line) for line in self.map])

    def __repr__(self):
        return self.__str__()


assert Guard(common.Loader.load_matrix('test')).patrol() == 41

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{Guard(common.Loader.load_matrix()).patrol()}{Fore.RESET}{Back.RESET}')