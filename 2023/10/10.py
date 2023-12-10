import common


# We start at start, find a tile that connects and then crawl along it until we reach start again
class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.start = self.find_start()
        self.crawl_pipe()

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
                return self.matrix[y][x] in ['|', 'L', 'J', 'S', '#'] and self.matrix[y+dy][x+dx] in ['|', 'F', '7', 'S', '#']
            elif dx == 0 and dy == 1:
                # this means we go "down"
                return self.matrix[y][x] in ['|', 'F', '7', 'S', '#'] and self.matrix[y + dy][x + dx] in ['|', 'L', 'J', 'S', '#']
            elif dx == -1 and dy == 0:
                # this means we go "left"
                return self.matrix[y][x] in ['-', 'J', '7', 'S', '#'] and self.matrix[y + dy][x + dx] in ['-', 'F', 'L', 'S', '#']
            elif dx == 1 and dy == 0:
                # this means we go "right"
                return self.matrix[y][x] in ['-', 'F', 'L', 'S', '#'] and self.matrix[y + dy][x + dx] in ['-', 'J', '7', 'S', '#']
        return False

    def replace_start(self):
        # if connects to top
        if self.connects(self.start[0], self.start[1], 0, -1):
            # if connects to bottom
            if self.connects(self.start[0], self.start[1], 0, 1):
                self.matrix[self.start[1]][self.start[0]] = '|'
            elif self.connects(self.start[0], self.start[1], -1, 0):
                self.matrix[self.start[1]][self.start[0]] = 'J'
            elif self.connects(self.start[0], self.start[1], 1, 0):
                self.matrix[self.start[1]][self.start[0]] = 'L'
        elif self.connects(self.start[0], self.start[1], 0, 1):
            if self.connects(self.start[0], self.start[1], -1, 0):
                self.matrix[self.start[1]][self.start[0]] = '7'
            elif self.connects(self.start[0], self.start[1], 1, 0):
                self.matrix[self.start[1]][self.start[0]] = 'F'
        elif self.connects(self.start[0], self.start[1], -1, 0):
            if self.connects(self.start[0], self.start[1], 1, 0):
                self.matrix[self.start[1]][self.start[0]] = '-'

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

        # new_matrix is to clean "dummy pipes"
        new_matrix = [['.' for _ in line] for line in self.matrix]
        new_matrix[self.start[1]][self.start[0]] = 'S'
        (px, py) = self.start
        (cx, cy) = self.find_next(-1, -1, self.start[0], self.start[1])
        while (cx, cy) != (-1, -1) and (cx, cy) != self.start:
            new_matrix[cy][cx] = self.matrix[cy][cx]
            (npx, npy) = (cx, cy)
            (cx, cy) = self.find_next(px, py, cx, cy)
            (px, py) = (npx, npy)

        if (cx, cy) == (-1, -1):
            raise Exception(f'Could not find a pipe from {px}:{py}!!')

        self.matrix = new_matrix
        self.replace_start()
        self.replace_area()

    def find_farthest_point(self):
        # length == count of # tiles
        return sum([sum([1 for _ in row if _ not in ['.', 'I']]) for row in self.matrix])//2

    def replace_area(self):
        # To be implemented
        for y in range(len(self.matrix)):
            enter = None
            is_in = False
            for x in range(len(self.matrix[y])):
                # I can enter on F, | or L
                # then depending on exit, I am in or not
                if self.matrix[y][x] == '-':
                    continue # skip pipes
                if self.matrix[y][x] == '|':
                    is_in = not is_in
                elif self.matrix[y][x] in ['F', 'L']:
                    if not is_in:
                        enter = self.matrix[y][x]
                        is_in = True
                    elif is_in:
                        enter = 'F' if self.matrix[y][x] == 'L' else 'L'
                elif self.matrix[y][x] in ['7', 'J'] and is_in:
                    if enter == 'F' and self.matrix[y][x] == '7':
                        is_in = False
                    if enter == 'L' and self.matrix[y][x] == 'J':
                        is_in = False
                else:
                    if is_in:
                        self.matrix[y][x] = 'I'

    def find_area(self):
        return sum([sum([1 for _ in row if _ == 'I']) for row in self.matrix])


    def __str__(self):
        return '\n'.join([''.join([_ for _ in row]) for row in self.matrix])

    def __repr__(self):
        return self.__str__()


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