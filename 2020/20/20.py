import re


class Tile:
    def __init__(self, buffer):
        self.number = int(buffer.pop(0)[5:-1])
        self.tile = buffer
        self.x = None
        self.y = None

    def compare(self, _x, _y, _map):
        if self.compare_rotations(_x, _y, _map):
            return True
        self.flip()
        if self.compare_rotations(_x, _y, _map):
            return True
        self.flip()
        return False

    def compare_rotations(self, _x, _y, _map):
        for i in range(0, 4):
            if self.compare_edges(_x, _y, _map):
                return True
            self.rotate_left()
        return False

    def compare_edges(self, _x, _y, _map):
        match = True
        for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (_x + ox, _y + oy) in _map:
                match = match & (self.get_edge((ox, oy)) == work_map[(_x + ox, _y + oy)].get_edge((-ox, -oy)))

        return match

    def get_edge(self, _type):
        if _type == (0, 1):
            return self.tile[-1]
        elif _type == (0, -1):
            return self.tile[0]
        elif _type == (-1, 0):
            return ''.join([x[0] for x in self.tile])
        elif _type == (1, 0):
            return ''.join([x[-1] for x in self.tile])
        raise Exception("Unexpected type!")

    def add_to_map(self, _x, _y, _map):
        self.x = _x
        self.y = _y
        _map[(_x, _y)] = self

    def rotate_left(self):
        new_tile = []
        for row in range(1, len(self.tile) + 1):
            new_tile.append(''.join([x[-row] for x in self.tile]))
        self.tile = new_tile

    def flip(self):
        self.tile.reverse()

    def count_char(self, _char):
        cnt = 0
        for line in self.tile:
            for char in line:
                if char == _char:
                    cnt +=1
        return cnt

    def __str__(self):
        return 'Tile #{}\n{}'.format(self.number, '\n'.join(self.tile))

    def __repr__(self):
        return 'Tile #{}'.format(self.number)


def find_monsters(_map):
    pattern = '..................#.' + '#....##....##....###' + '.#..#..#..#..#..#...'
    monster_count = 15
    for i in range(0, 4):
        cnt = search_map_for_monsters(full_map, pattern)
        if cnt > 0:
            return _map.count_char('#') - monster_count * cnt
        full_map.rotate_left()
    full_map.flip()
    for i in range(0, 4):
        cnt = search_map_for_monsters(full_map, pattern)
        if cnt > 0:
            return _map.count_char('#') - monster_count * cnt
        full_map.rotate_left()
    raise Exception('Something went wrong, no monsters were found!')


def search_map_for_monsters(_map, _pattern):
    monster_locator = re.compile(_pattern)
    cnt = 0
    for ey in range(0, len(_map.tile) - 2):
        for ex in range(0, len(_map.tile) - 19):
            mask = _map.tile[ey][ex:ex + 20] + _map.tile[ey + 1][ex:ex + 20] + _map.tile[ey + 2][ex:ex + 20]
            if monster_locator.fullmatch(mask):
                cnt += 1
    return cnt


def read_file(_name):
    line_buffer = []
    temp_tiles = []
    for line in open(_name, 'r').readlines():
        line = line.strip()
        if len(line) == 0:
            if len(line_buffer) > 0:
                temp_tiles.append(Tile(line_buffer))
                line_buffer = []
        else:
            line_buffer.append(line)
    if len(line_buffer) > 0:
        temp_tiles.append(Tile(line_buffer))
    return temp_tiles


tiles = read_file('20.txt')
print(tiles)

work_map = {}
tiles.pop(0).add_to_map(0, 0, work_map)
stack = [(0, 0)]

while len(stack) > 0:
    cur = work_map[stack.pop(0)]
    for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        cx = dx + cur.x
        cy = dy + cur.y
        if (cx, cy) not in work_map:
            for tile in tiles:
                if tile.compare(cx, cy, work_map):
                    stack.append((cx, cy))
                    tile.add_to_map(cx, cy, work_map)
                    break
            if (cx, cy) in work_map:
                tiles.remove(work_map[(cx, cy)])

print(work_map)

max_x = 0
max_y = 0
min_x = 0
min_y = 0
for x, y in work_map.keys():
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    min_x = min(min_x, x)
    min_y = min(min_y, y)

# part one
result = work_map[(min_x, min_y)].number * work_map[(min_x, max_y)].number * work_map[(max_x, min_y)].number * work_map[(max_x, max_y)].number
print(result)

# combine map
result_buffer = ['Tile 13:']
side = len(work_map[(0, 0)].tile)
for y in range(min_y, max_y + 1):
    for line in range(1, side - 1):
        buffer = ''
        for x in range(min_x, max_x + 1):
            buffer += work_map[(x, y)].tile[line][1:-1]
        result_buffer.append(buffer)

full_map = Tile(result_buffer)
print(full_map)

# now look for monsters - hehe!
print(find_monsters(full_map))