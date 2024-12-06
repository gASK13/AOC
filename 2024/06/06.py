import common
from colorama import Fore, Back
from enum import Enum

DIRECTIONS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
ORDER = ['^', '>', 'v', '<']

class Result(Enum):
    LOOP = 1
    EXIT = 2
    STEP = 3

class Guard:
    def __init__(self, _map):
        self.old_x = None
        self.old_y = None
        self.old_map = None
        self.old_hits = None
        self.hits = {}
        self.map = _map
        self.obstacles = set()
        for idy, line in enumerate(_map):
            if '^' in line:
                self.x = line.index('^')
                self.y = idy
                break
        self.ox = self.x
        self.oy = self.y
        self.lda = False

    def start_loop_detection(self):
        self.old_map = [line.copy() for line in self.map]
        self.old_x = self.x
        self.old_y = self.y
        self.hits = {}
        self.lda = True

    def end_loop_detection(self):
        self.map = self.old_map
        self.x = self.old_x
        self.y = self.old_y
        self.old_map = None
        self.old_x = None
        self.old_y = None
        self.lda = False

    def patrol(self):
        while True:
            step = self.step()
            if step != Result.STEP:
                return step, sum([line.count('X') for line in self.map])

    def find_loop_count(self):
        # We might want to place it "before" the start as well!
        while True:
            direction = self.map[self.y][self.x]
            dx, dy = DIRECTIONS[direction]
            if (self.x + dx != self.ox or self.y + dy != self.oy) and len(self.map[0]) > self.x + dx >= 0 and len(self.map) > self.y + dy >= 0 and self.map[self.y + dy][self.x + dx] == '.':
                self.start_loop_detection()
                pos = (self.x + dx, self.y + dy)
                self.map[self.y + dy][self.x + dx] = '#'
                result, count = self.patrol()
                if result == Result.LOOP:
                    #self.print_obstacle(*pos)
                    self.obstacles.add(pos)
                self.end_loop_detection()
            if self.step() == Result.EXIT:
                break
        return len(self.obstacles)

    def step(self):
        direction = self.map[self.y][self.x]
        dx, dy = DIRECTIONS[direction]

        # Exiting map
        if self.x + dx < 0 or self.y + dy < 0 or self.x + dx >= len(self.map[0]) or self.y + dy >= len(self.map):
            self.map[self.y][self.x] = 'X'
            return Result.EXIT

        # Hit a wall
        if self.map[self.y + dy][self.x + dx] == '#':

            # Loop detection
            if self.lda:
                if (self.x + dx, self.y + dy) not in self.hits:
                    self.hits[(self.x + dx, self.y + dy)] = []
                if direction in self.hits[(self.x + dx, self.y + dy)]:
                    return Result.LOOP
                self.hits[(self.x + dx, self.y + dy)].append(direction)

            # Rotate
            self.map[self.y][self.x] = ORDER[(ORDER.index(direction) + 1) % len(ORDER)]
        else:
            # Just move on
            self.x += dx
            self.y += dy
            self.map[self.y][self.x] = self.map[self.y - dy][self.x - dx]
            self.map[self.y - dy][self.x - dx] = 'X' if not self.lda else f'{Fore.RED}o{Fore.RESET}'
        return Result.STEP

    def print_obstacle(self, ox, oy):
        print(f'\n\nFound obstacle at {ox}, {oy}')
        print('\n'.join([''.join([f'{Fore.GREEN}@{Fore.RESET}' if x == ox and y == oy else c for x, c in enumerate(line)]) for y, line in enumerate(self.map)]))

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.map])

    def __repr__(self):
        return self.__str__()


assert Guard(common.Loader.load_matrix('test')).patrol()[1] == 41

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{Guard(common.Loader.load_matrix()).patrol()[1]}{Fore.RESET}{Back.RESET}')

assert Guard(common.Loader.load_matrix('test')).find_loop_count() == 6

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{Guard(common.Loader.load_matrix()).find_loop_count()}{Fore.RESET}{Back.RESET}')