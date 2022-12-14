import common

class Map:
    def __init__(self, lines):
        self.map = {}
        self.minx = 0
        self.maxx = 0
        self.miny = 0
        self.maxy = 0
        for line in lines:
            coords = [[int(c) for c in coord.split(',')] for coord in line.split(' -> ')]
            for i in range(len(coords) - 1):
                self.line(coords[i], coords[i+1])
        self.reset_range_x()
        (self.miny, self.maxy) = sorted([y for (x, y) in self.map])[::len(self.map) - 1]
        self.maxy += 1

    def grain_count(self):
        return len([1 for value in self.map.values() if value == 'o'])

    def line(self, start, end):
        (minx, maxx) = sorted([start[0], end[0]])
        (miny, maxy) = sorted([start[1], end[1]])
        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                self.map[(x, y)] = '#'

    def reset_range_x(self):
        (self.minx, self.maxx) = sorted([x for (x, y) in self.map])[::len(self.map) - 1]

    def run(self, floor=False):
        while self.flow(floor):
            pass
        return self.grain_count()

    def flow(self, floor=False):
        grain = (500, 0)

        if grain in self.map:
            return False #we are full!

        while grain[1] < self.maxy:
            # move grain
            new_grain = None
            for move in [(0, 1), (-1, 1), (1, 1)]:
                if (grain[0] + move[0], grain[1] + move[1]) not in self.map:
                    new_grain = (grain[0] + move[0], grain[1] + move[1])
                    break
            if new_grain is None:
                self.map[grain] = 'o'
                self.reset_range_x()
                return True
            grain = new_grain

        #fell off
        if floor:
            self.map[grain] = 'o'
            self.reset_range_x()
            return True
        return False

    def __str__(self):
        repr = ''
        for y in range(self.miny, self.maxy + 1):
            for x in range(self.minx, self.maxx + 1):
                repr += self.map[(x,y)] if (x, y) in self.map else ' '
            repr += '\n'
        return repr

    def __repr__(self):
        return str(self)


assert Map(['498,4 -> 498,6 -> 496,6', '503,4 -> 502,4 -> 502,9 -> 494,9']).run() == 24
print(f'Grain count for 1st is {Map(common.Loader.load_lines()).run()}')

assert Map(['498,4 -> 498,6 -> 496,6', '503,4 -> 502,4 -> 502,9 -> 494,9']).run(True) == 93
print(f'Grain count for 1st is {Map(common.Loader.load_lines()).run(True)}')

