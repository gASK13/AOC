import common


def get_matrix(size, glitch):
    matrix = [[False for x in range(size)] for y in range(size)]
    if glitch:
        matrix[0][0] = True
        matrix[0][size-1] = True
        matrix[size-1][0] = True
        matrix[size-1][size-1] = True
    return matrix


class LightGrid:
    def __init__(self, matrix, glitch=False):
        self.size = len(matrix)
        self.grid = get_matrix(self.size, glitch)
        self.glitch = glitch
        for x in range(self.size):
            for y in range(self.size):
                if matrix[y][x] == '#':
                    self.grid[y][x] = True

    def get_light_count(self):
        return sum([sum([1 for x in range(self.size) if self.grid[y][x]]) for y in range(self.size)])

    def get_neighbor_state_count(self, x, y):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x+dx < self.size and 0 <= y+dy < self.size and (dx != 0 or dy != 0):
                    if self.grid[y+dy][x+dx]:
                        count += 1
        return count

    def animate(self):
        _new_grid = get_matrix(self.size, self.glitch)
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[y][x]:
                    if self.get_neighbor_state_count(x, y) in [2, 3]:
                        _new_grid[y][x] = True
                else:
                    if self.get_neighbor_state_count(x, y) == 3:
                        _new_grid[y][x] = True
        self.grid = _new_grid

    def __repr__(self):
        return '\n'.join([''.join(['#' if self.grid[y][x] else '.' for x in range(self.size)]) for y in range(self.size)]) + '\n'

    def __str__(self):
        return self.__repr__()


lg = LightGrid(common.Loader.load_matrix('test'))
assert lg.get_light_count() == 15
lg.animate()
assert lg.get_light_count() == 11
lg.animate()
assert lg.get_light_count() == 8
lg.animate()
assert lg.get_light_count() == 4
lg.animate()
assert lg.get_light_count() == 4

lg = LightGrid(common.Loader.load_matrix('test'), True)
for i in range(5):
    lg.animate()
assert lg.get_light_count() == 17

lg = LightGrid(common.Loader.load_matrix())
for i in range(100):
    lg.animate()
print(f'Part 1: {lg.get_light_count()}')

lg = LightGrid(common.Loader.load_matrix(), True)
for i in range(100):
    lg.animate()
print(f'Part 2: {lg.get_light_count()}')