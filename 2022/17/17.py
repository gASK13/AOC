import common

class Map:
    def __init__(self):
        self.full = []
        self.top = -1
        self.offset = 0

    def hash_rows(self):
        cnt = 5000
        if self.top > cnt:
            return '#'.join([''.join(x) for x in self.full[-5000:]])
        return None

    def get_spawn_height(self):
        # get highest self.full
        return self.top + 4

    def rest_shape(self, shape):
        for piece in shape.pieces:
            while piece[1] + shape.y > self.top:
                self.top += 1
                self.full.append(['_' for i in range(7)])
            self.full[piece[1] + shape.y][piece[0] + shape.x] = '#'

    def is_full(self, x, y):
        return y < 0 or x < 0 or x > 6 or (y <= self.top and self.full[y][x] == '#')


class Shape:
    def __init__(self, pieces, bottom):
        self.pieces = pieces
        self.x = 2
        self.y = bottom

    def move(self, map, direction=(0, -1), rest=True):
        for piece in self.pieces:
            if map.is_full(piece[0] + self.x + direction[0], piece[1] + self.y + direction[1]):
                if rest:
                    map.rest_shape(self)
                    return False
                return True
        self.x += direction[0]
        self.y += direction[1]
        return True


pieces = [[(0, 0), (1, 0), (2, 0), (3, 0)],
          [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
          [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
          [(0, 0), (0, 1), (0, 2), (0, 3)],
          [(0, 0), (1, 0), (1, 1), (0, 1)]]

jets = {'<': (-1, 0), '>': (1, 0)}


def fall(_jets, rock_count):
    map = Map()
    jet_idx = 0
    cache = {}
    finished = False
    i = 0
    while i < rock_count:
        rock = Shape(pieces[i % len(pieces)], map.get_spawn_height())
        while True:
            jet = _jets[jet_idx]
            jet_idx += 1
            jet_idx %= len(_jets)
            rock.move(map, jets[jet], False)
            if not rock.move(map):
                if not finished:
                    hsh = map.hash_rows()
                    if hsh is not None:
                        if hsh in cache:
                            last_i, last_top = cache[hsh]
                            delta_i = i - last_i
                            print(f'JACKPOT - {delta_i} at {i} for {map.top - last_top}!')
                            reps = (rock_count - i) // delta_i
                            i += reps * delta_i
                            map.offset = reps * (map.top - last_top)
                            finished = True
                        else:
                            cache[hsh] = (i, map.top)
                break
        i += 1
    print(map.top + map.offset + 1)
    return map.top + map.offset + 1

assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 1) == 1
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 2) == 4
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 3) == 6
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 4) == 7
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 5) == 9
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 6) == 10
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 7) == 13
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 8) == 15
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 9) == 17
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 10) == 17
assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 2022) == 3068
print(f'First part: {fall(common.Loader.load_lines()[0], 2022)}')


assert fall('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 1000000000000) == 1514285714288
print(f'Second part: {fall(common.Loader.load_lines()[0], 1000000000000)}')