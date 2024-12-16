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

    def can_push(self, bx, by, dx, dy, testOnly=False):
        if self.map[by][bx] == 'O':
            if (self.map[by + dy][bx + dx] == '.'
                    or (self.map[by + dy][bx + dx] in ['O', '[', ']'] and self.can_push(bx + dx, by + dy, dx, dy))):
                if not testOnly:
                    self.map[by + dy][bx + dx] = 'O'
                    self.map[by][bx] = '.'
                return True
        if self.map[by][bx] in ['[', ']']:
            if dy == 0:
                # left / right
                if (self.map[by + dy][bx + dx*2] == '.'
                        or (self.map[by + dy][bx + dx*2] in ['O', '[', ']'] and self.can_push(bx + dx*2, by + dy, dx, dy))):
                    if not testOnly:
                        self.map[by + dy][min(bx + dx, bx+dx*2)] = '['
                        self.map[by + dy][max(bx + dx, bx+dx*2)] = ']'
                        self.map[by][bx] = '.'
                    return True
            else:
                mx = 1 if self.map[by][bx] == '[' else -1
                # empty space or boxes that can push further
                # I need "prepush" check - all or nothing :(
                if ((self.map[by + dy][bx] == '.' or (self.map[by + dy][bx] in ['O', '[', ']'] and self.can_push(bx, by + dy, dx, dy, True)))
                    and (self.map[by + dy][bx + mx] == '.' or (self.map[by + dy][bx + mx] in ['O', '[', ']'] and self.can_push(bx + mx, by + dy, dx, dy, True)))):
                    if not testOnly:
                        if self.map[by + dy][bx] in ['O', '[', ']']:
                            self.can_push(bx, by + dy, dx, dy)
                        if self.map[by + dy][bx + mx] in ['O', '[', ']']:
                            self.can_push(bx + mx, by + dy, dx, dy)
                        self.map[by + dy][min(bx, bx + mx)] = '['
                        self.map[by + dy][max(bx, bx + mx)] = ']'
                        self.map[by][bx] = '.'
                        self.map[by][bx+mx] = '.'
                    return True
        pass

    def move(self, move):
        dx, dy = MOVES[move]
        sx = self.player[0]
        sy = self.player[1]
        # try to use "recursion" (push the next box)
        if (self.map[sy + dy][sx + dx] == '.'
                or (self.map[sy + dy][sx + dx] in ['O', '[', ']'] and self.can_push(sx + dx, sy + dy, dx, dy))):
            self.map[sy][sx] = '.'
            self.map[sy + dy][sx + dx] = '@'
            self.player = (self.player[0] + dx, self.player[1] + dy)

    def score(self):
        # 100 * y + x
        return sum([100 * idy + idx for idy, line in enumerate(self.map) for idx, char in enumerate(line) if char in ['O', '[']])

    def __str__(self):
        return '\n'.join([''.join([c if c != '@' else f'{Fore.GREEN}{c}{Fore.RESET}' for c in line]) for line in self.map])

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

def expand(line):
    out = ''
    for char in line:
        match char:
            case '.':
                out += '..'
            case '#':
                out += '##'
            case 'O':
                out += '[]'
            case '@':
                out += '@.'
    return out

def part_two(input):
    _map = []
    while len(input[0]) > 0:
        _map.append(list(expand(input[0])))
        input.pop(0)

    # run steps
    s = Sokoban(_map)
    for line in input:
        for c in line:
            s.move(c)

    return s.score()



assert part_one(common.Loader.load_lines('test_s')) == 2028
assert part_one(common.Loader.load_lines('test')) == 10092
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Back.RESET}{Fore.RESET}')

assert part_two(common.Loader.load_lines('test_s2')) == 105 + 207 + 306
assert part_two(common.Loader.load_lines('test')) == 9021
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Back.RESET}{Fore.RESET}')