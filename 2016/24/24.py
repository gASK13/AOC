import common


class Place:
    def __init__(self, x, y, id):
        self.id = id
        self.x = x
        self.y = y
        self.distances = {}

    def __str__(self):
        return f'{self.id}@{self.x},{self.y} => {self.distances}'


class Map:
    def __init__(self, lines):
        self.indices = {}
        self.traversable = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char in '01234567890.':
                    self.traversable[(x,y)] = char
                    if char in '0123456789':
                        self.indices[char] = Place(x, y, char)
        self.build_paths()

    def build_paths(self):
        for idx in self.indices:
            self.build_path(self.indices[idx])

    def build_path(self, place):
        seen = {(place.x, place.y)}
        buffer = [(place.x, place.y, 0)]
        while len(buffer) > 0:
            x, y, dist = buffer.pop(0)
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                if (x+dx, y+dy) in self.traversable and (x+dx, y+dy) not in seen:
                    buffer.append((x + dx, y + dy, dist + 1))
                    seen.add((x+dx, y+dy))
                    if self.traversable[(x+dx, y+dy)] in '0123456789':
                        place.distances[self.traversable[(x+dx, y+dy)]] = dist + 1

    def get_shortest_route(self, goback=False):
        buffer = [(self.indices['0'], ['0'], 0)]
        min_steps = 99999999
        while len(buffer) > 0:
            place, visited, steps = buffer.pop(0)
            stop = True
            for p in place.distances:
                if p not in visited:
                    buffer.append((self.indices[p], visited + [p], steps + place.distances[p]))
                    stop = False
            if stop:
                min_steps = min([steps + (place.distances['0'] if goback else 0), min_steps])
        return min_steps


assert Map(common.Loader.load_lines('test')).get_shortest_route() == 14
print(f'Shortes route to visit all is {Map(common.Loader.load_lines()).get_shortest_route()}')

assert Map(common.Loader.load_lines('test')).get_shortest_route(True) == 20
print(f'Shortest route to visit all and get back is {Map(common.Loader.load_lines()).get_shortest_route(True)}')

