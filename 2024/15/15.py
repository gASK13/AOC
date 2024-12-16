import common
from colorama import Fore,Back

MOVES = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}

class Sokoban:
    def __init__(self, _map):
        self.map = _map
        self.player = (0, 0)
        for idy, line in enumerate(self.map):
            for idx, char in enumerate(line):
                if char == '@':
                    self.player = (idx, idy)
                    break

    def move(self, move):
        dx, dy = MOVES[move]
        sx = self.player[0]
        sy = self.player[1]
        push = False
        while self.map[sy + dy][sx + dx] != '#':
            if self.map[sy + dy][sx + dx] == '.':
                if push:
                    self.map[sy + dy][sx + dx] = 'O'
                self.map[self.player[1]][self.player[0]] = '.'
                self.map[self.player[1] + dy][self.player[0] + dx] = '@'
                self.player = (self.player[0] + dx, self.player[1] + dy)
                return
            if self.map[sy + dy][sx + dx] == 'O':
                push = True
            sx += dx
            sy += dy
        # option 1 - just .
        # option 2 - there are O and then .
        # option 3 - there is wall anywhere
        pass

    def score(self):
        # 100 * y + x
        return sum([100 * idy + idx for idy, line in enumerate(self.map) for idx, char in enumerate(line) if char == 'O'])

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.map])

    def __repr__(self):
        return self.__str__()

def part_one(input):
    _map = []
    while len(input[0]) > 0:
        _map.append(list(input[0]))
        input.pop(0)

    # run steps
    s = Sokoban(_map)
    for line in input:
        for c in line:
            s.move(c)

    return s.score()

def part_two(input):
    pass


assert part_one(common.Loader.load_lines('test_s')) == 2028
assert part_one(common.Loader.load_lines('test')) == 10092
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Back.RESET}{Fore.RESET}')