import common
from colorama import Fore,Back

def turns(vector):
    x, y = vector
    return [(y, -x), (-y, x)]


class Maze:
    def __init__(self, matrix):
        self.maze = matrix
        self.x = 0
        self.y = 0
        self.ex = 0
        self.ey = 0
        for idy, item in enumerate(self.maze):
            for idx, char in enumerate(item):
                if char == 'E':
                    self.ex = idx
                    self.ey = idy
                    self.maze[idy][idx] = '.'
                if char == 'S':
                    self.x = idx
                    self.y = idy
                    self.maze[idy][idx] = '.'

    def part_one(self):
        return self.solve_lowest()[0]

    def part_two(self):
        return len(self.solve_lowest()[1])

    def solve_lowest(self):
        buffer = [(self.x, self.y, 0, 1, 0, [])]
        visited = set()
        while len(buffer) > 0:
            x, y, s, vx, vy, path = buffer.pop(0)
            if x == self.ex and y == self.ey:
                final_p = set()
                final_p.add((x, y))
                for i in path:
                    final_p.add(i)
                while buffer[0][2] == s:
                    x, y, s, vx, vy, path = buffer.pop(0)
                    if x == self.ex and y == self.ey:
                        for i in path:
                            final_p.add(i)
                return s, final_p
            visited.add((x, y, vx, vy))
            if 0 <= x+vx < len(self.maze[0]) and 0 <= y+vy < len(self.maze) and self.maze[y+vy][x+vx] == '.':
                if (x+vx, y+vy, vx, vy) not in visited:
                    buffer.append((x+vx, y+vy, s+1, vx, vy, path + [(x, y)]))
            for turn in turns((vx, vy)):
                if (x, y, turn[0], turn[1]) not in visited:
                    buffer.append((x, y, s+1000, turn[0], turn[1], path))
            # sort by third key
            buffer.sort(key=lambda x: x[2])
        return -1, set()

assert Maze(common.Loader.load_matrix('test_7036')).part_one() == 7036
assert Maze(common.Loader.load_matrix('test_11048')).part_one() == 11048

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{Maze(common.Loader.load_matrix()).part_one()}{Back.RESET}{Fore.RESET}')


assert Maze(common.Loader.load_matrix('test_7036')).part_two() == 45
assert Maze(common.Loader.load_matrix('test_11048')).part_two() == 64

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{Maze(common.Loader.load_matrix()).part_two()}{Back.RESET}{Fore.RESET}')
