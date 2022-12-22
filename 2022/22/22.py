import common


class Tile:
    def __init__(self, x, y, wall):
        self.wall = wall
        self.x = x
        self.y = y
        self.directions = {(1, 0): [None, 'x'], (0, 1): [None, 'x'], (-1, 0): [None, 'x'], (0, -1): [None, 'x']}

    def value(self):
        return 1000 * (self.y+1) + 4 * (self.x+1)


class Board:
    def __init__(self, lines, cube=None):
        # last line is instructions, before is blank
        self.instructions = lines.pop()
        lines.pop()
        # now build map
        cols = {}
        self.tile = None
        self.direction = (1, 0)
        self.idx = {}
        for (y, line) in enumerate(lines):
            last_tile = None
            first_tile = None
            for (x, char) in enumerate(line):
                if char == '#' or char == '.':
                    tile = Tile(x, y, char == '#')
                    self.idx[(x, y)] = tile
                    # set start
                    if self.tile is None and char == '.':
                        self.tile = tile
                    # for wrapround
                    if first_tile is None:
                        first_tile = tile
                    # connect going to left
                    if last_tile is not None:
                        last_tile.directions[(1, 0)][0] = tile
                        tile.directions[(-1, 0)][0] = last_tile
                    if x not in cols:
                        cols[x] = []
                    cols[x].append(tile)
                    last_tile = tile
            # wrapround
            if first_tile is not None:
                last_tile.directions[(1, 0)][0] = first_tile
                first_tile.directions[(-1, 0)][0] = last_tile
        # now connect by columns
        for column in cols.values():
            for i in range(len(column)):
                column[i-1].directions[(0, -1)][0] = column[i]
                column[i].directions[(0, 1)][0] = column[i-1]
        if cube is not None:
            # wow, now let's wrap this into a cube - identify sides and rewrap
            width = max([len(line) for line in lines])
            height = len(lines)
            self.sidesize = max([height, width]) // 4
            if cube == 'test':
                self.connect_tiles(self.get_tiles(2, 0, 'LEFT'), self.get_tiles(1, 1, 'TOP'), (-1, 0), (0, 1), 'L', 'R')
                self.connect_tiles(self.get_tiles(2, 0, 'RIGHT'), self.get_tiles(3, 2, 'RIGHT', True), (1, 0), (1, 0),
                                   'S', 'S')
                self.connect_tiles(self.get_tiles(2, 0, 'TOP'), self.get_tiles(0, 1, 'TOP', True), (0, 1), (0, 1),
                                   'S', 'S')
                self.connect_tiles(self.get_tiles(0, 1, 'BOTTOM'), self.get_tiles(2, 2, 'BOTTOM', True), (0, -1), (0, -1),
                                   'S', 'S')
                self.connect_tiles(self.get_tiles(0, 1, 'LEFT'), self.get_tiles(3, 2, 'BOTTOM', True), (-1, 0), (0, 1),
                                   'R', 'L')
                self.connect_tiles(self.get_tiles(1, 1, 'BOTTOM'), self.get_tiles(2, 2, 'LEFT', True), (0, -1), (-1, 0),
                                   'L', 'R')
                self.connect_tiles(self.get_tiles(2, 1, 'RIGHT'), self.get_tiles(3, 2, 'TOP', True), (1, 0), (0, 1),
                                   'R', 'L')
                pass
            if cube == 'input':
                pass
                self.connect_tiles(self.get_tiles(1, 0, 'LEFT'), self.get_tiles(0, 2, 'LEFT', True), (-1, 0), (-1, 0),
                                   'S', 'S')
                self.connect_tiles(self.get_tiles(0, 3, 'LEFT'), self.get_tiles(1, 0, 'TOP'), (-1, 0), (0, 1), 'L', 'R')
                self.connect_tiles(self.get_tiles(2, 0, 'TOP'), self.get_tiles(0, 3, 'BOTTOM'), (0, 1), (0, -1), 'x', 'x')
                self.connect_tiles(self.get_tiles(2, 0, 'BOTTOM'), self.get_tiles(1, 1, 'RIGHT'), (0, -1), (1, 0),
                                   'R', 'L')
                self.connect_tiles(self.get_tiles(2, 0, 'RIGHT'), self.get_tiles(1, 2, 'RIGHT', True), (1, 0), (1, 0),
                                   'S', 'S')
                self.connect_tiles(self.get_tiles(1, 1, 'LEFT'), self.get_tiles(0, 2, 'TOP'), (-1, 0), (0, 1), 'L', 'R')
                self.connect_tiles(self.get_tiles(1, 2, 'BOTTOM'), self.get_tiles(0, 3, 'RIGHT'), (0, -1), (1, 0),
                                   'R', 'L')
            # Ok, so I hard coded the connections, sue me

    def get_tiles(self, x, y, s, swap=False):
        tiles = []
        match s:
            case 'LEFT':
                tiles = [self.idx[(x*self.sidesize, y*self.sidesize + yi)] for yi in range(self.sidesize)]
            case 'RIGHT':
                tiles = [self.idx[((x + 1) * self.sidesize - 1, y * self.sidesize + yi)] for yi in range(self.sidesize)]
            case 'TOP':
                tiles = [self.idx[(x*self.sidesize + xi, y*self.sidesize)] for xi in range(self.sidesize)]
            case 'BOTTOM':
                tiles = [self.idx[(x*self.sidesize + xi, (y + 1)*self.sidesize - 1)] for xi in range(self.sidesize)]
        return tiles if not swap else [r for r in reversed(tiles)]

    def connect_tiles(self, st, tt, sd, td, sr, tr):
        # example - sd is (-1,0) and td is (0, 1)
        # rotation should be for SD "L" and for td "R"

        # example - sd is (1, 0) and td id (1, 0)
        # rotation should be 'S' for both

        for i in range(len(st)):
            st[i].directions[sd] = [tt[i], sr]
            tt[i].directions[td] = [st[i], tr]

    def rotate(self, direction):
        match direction:
            case 'R':
                self.direction = (self.direction[1], -self.direction[0])
            case 'L':
                self.direction = (-self.direction[1], self.direction[0])
            case 'S':
                self.direction = (-self.direction[0], -self.direction[1])

    def move(self, steps):
        for m in range(steps):
            if not self.tile.directions[self.direction][0].wall:
                rot = self.tile.directions[self.direction][1]
                self.tile = self.tile.directions[self.direction][0]
                self.rotate(rot)

    def process(self):
        num = '0'
        for i in self.instructions:
            if i == 'R' or i == 'L':
                self.move(int(num))
                self.rotate(i)
                num = '0'
            else:
                num += i
        self.move(int(num))
        return self.tile.value() + {(1, 0): 0, (0, 1): 3, (-1, 0): 2, (0, -1): 4}[self.direction]


assert Board(common.Loader.load_lines('test', strip=False)).process() == 6032
print(f'First part is {Board(common.Loader.load_lines(strip=False)).process()}')

assert Board(common.Loader.load_lines('test', strip=False), cube='test').process() == 5031
print(f'First part is {Board(common.Loader.load_lines(strip=False), cube="input").process()}')




