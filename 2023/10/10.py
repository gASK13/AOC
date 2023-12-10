import common


# We start at start, find a tile that connects and then crawl along it until we reach start again
class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.start = self.find_start()

    def find_start(self):
        # start is a tile with 'S' in the matrix
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] == 'S':
                    return (x, y)

    def connects(self, x, y, dx, dy):
        if 0 <= x + dx < len(self.matrix[y]) and 0 <= y + dy < len(self.matrix):
            if dx == 0 and dy == -1:
                # this means we go "up"
                return self.matrix[y][x] in ['|', 'L', 'J', 'S'] and self.matrix[y+dy][x+dx] in ['|', 'F', '7', 'S']
            elif dx == 0 and dy == 1:
                # this means we go "down"
                return self.matrix[y][x] in ['|', 'F', '7', 'S'] and self.matrix[y + dy][x + dx] in ['|', 'L', 'J', 'S']
            elif dx == -1 and dy == 0:
                # this means we go "left"
                return self.matrix[y][x] in ['-', 'J', '7', 'S'] and self.matrix[y + dy][x + dx] in ['-', 'F', 'L', 'S']
            elif dx == 1 and dy == 0:
                # this means we go "right"
                return self.matrix[y][x] in ['-', 'F', 'L', 'S'] and self.matrix[y + dy][x + dx] in ['-', 'J', '7', 'S']
        return False

    def find_next(self, px, py, cx, cy):
        for (dx, dy) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if cx + dx == px and cy + dy == py:
                continue # do not cycle back and forth
            if self.connects(cx, cy, dx, dy):
                return cx + dx, cy + dy
        return -1, -1

    def crawl_pipe(self):
        # start at start and first look into the four directions above
        # if we find a tile that connects, we crawl along it until we reach start again
        (px, py) = self.start
        (cx, cy) = self.find_next(-1, -1, self.start[0], self.start[1])
        pl = 1
        while (cx, cy) != (-1, -1) and (cx, cy) != self.start:
            (npx, npy) = (cx, cy)
            (cx, cy) = self.find_next(px, py, cx, cy)
            (px, py) = (npx, npy)
            pl += 1
        if (cx, cy) == (-1, -1):
            raise Exception(f'Could not find a pipe from {px}:{py}!!')
        return pl

    def find_farthest_point(self):
        return self.crawl_pipe() / 2

    def find_area(self):
        # To be implemented
        return None


assert Map(common.Loader.load_matrix('test1')).find_farthest_point() == 4
assert Map(common.Loader.load_matrix('test2')).find_farthest_point() == 4
assert Map(common.Loader.load_matrix('test3')).find_farthest_point() == 8

print(f'Part 1: {Map(common.Loader.load_matrix()).find_farthest_point()}')

assert Map(common.Loader.load_matrix('test1')).find_area() == 1
assert Map(common.Loader.load_matrix('test2')).find_area() == 1
assert Map(common.Loader.load_matrix('test3')).find_area() == 1
assert Map(common.Loader.load_matrix('test_p2')).find_area() == 4
assert Map(common.Loader.load_matrix('test_p2_2')).find_area() == 4
assert Map(common.Loader.load_matrix('test_p2_3')).find_area() == 8
assert Map(common.Loader.load_matrix('test_p2_4')).find_area() == 10

print(f'Part 2: {Map(common.Loader.load_matrix()).find_area()}')