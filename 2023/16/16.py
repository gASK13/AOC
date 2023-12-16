import common
from colorama import Fore, Back, Style


class Grid:
    def __init__(self, matrix, variable=False):
        self.grid = matrix
        if variable:
            self.energy = max([self.run_beam((0, i, 1, 0)) for i in range(len(self.grid))])
            self.energy = max([self.energy] + [self.run_beam((len(self.grid[0]) - 1, i, -1, 0)) for i in range(len(self.grid))])
            self.energy = max(
                [self.energy] + [self.run_beam((i, len(self.grid) - 1, 0, -1)) for i in range(len(self.grid[0]))])
            self.energy = max(
                [self.energy] + [self.run_beam((i, 0, 0, 1)) for i in range(len(self.grid[0]))])
        else:
            self.energy = self.run_beam()

    def run_beam(self, start=(0, 0, 1, 0)):
        energized = [[False for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        beams = [start]
        seen = set()
        while len(beams) > 0:
            bx, by, bdx, bdy = beams.pop()
            # first skip already seen and out of bounds
            if (bx, by, bdx, bdy) in seen:
                continue
            if bx < 0 or by < 0 or bx >= len(self.grid[0]) or by >= len(self.grid):
                continue

            # add to already seen
            seen.add((bx, by, bdx, bdy))
            energized[by][bx] = True
            match self.grid[by][bx]:
                case '.':
                    beams.append((bx + bdx, by + bdy, bdx, bdy))
                case '\\':
                    beams.append((bx + bdy, by + bdx, bdy, bdx))
                case '/':
                    beams.append((bx - bdy, by - bdx, -bdy, -bdx))
                case '-':
                    if bdy != 0:
                        beams.append((bx - 1, by, -1, 0))
                        beams.append((bx + 1, by, 1, 0))
                    else:
                        beams.append((bx + bdx, by + bdy, bdx, bdy))
                case '|':
                    if bdx != 0:
                        beams.append((bx, by - 1, 0, -1))
                        beams.append((bx, by + 1, 0, 1))
                    else:
                        beams.append((bx + bdx, by + bdy, bdx, bdy))
        return sum([sum([1 if _ else 0 for _ in row]) for row in energized])

    def __str__(self):
        return '\n'.join([''.join(['#' if _ else '.' for _ in row]) for row in self.energized])

    def __repr__(self):
        return self.__str__()


assert Grid(common.Loader.load_matrix('test')).energy == 46

print(f'Part 1: {Back.GREEN}{Fore.BLACK}{Grid(common.Loader.load_matrix()).energy}')

assert Grid(common.Loader.load_matrix('test'), True).energy == 51

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{Grid(common.Loader.load_matrix(), True).energy}')