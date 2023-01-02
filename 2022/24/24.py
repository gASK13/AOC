import common


class Map:
    def __init__(self, lines=None, o=None):
        if o is not None:
            self.step = o.step
            self.dimensions = o.dimensions
            self.tornadoes = o.tornadoes
            self.position = o.position
            self.start = o.start
            self.exit = o.exit
            self.target = o.target
            self.state = o.state
        else:
            self.tornadoes = {0: {}}
            self.step = 0
            self.dimensions = (len(lines[0]), len(lines))
            translator = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
            for (y, line) in enumerate(lines):
                for (x, char) in enumerate(line):
                    if char == '.':
                        if y == 0:
                            self.position = (x, y)
                            self.start = (x, y)
                        if y == len(lines) - 1:
                            self.exit = (x, y)
                    if char in '><v^':
                        if (x, y) not in self.tornadoes[0]:
                            self.tornadoes[0][(x,y)] = []
                        self.tornadoes[0][(x, y)].append(translator[char])
            self.target = self.exit
            self.state = 0

    def __repr__(self):
        return f'EMAP'

    def __hash__(self):
        return self.position[0] * 100000000 + self.position[1] * 100000 + self.step * 10 + self.state

    def __eq__(self, other):
        return self.position == other.position and self.step == other.step and self.state == other.state

    def turn(self, adv=False):
        self.step += 1
        if self.step not in self.tornadoes:
            new_ts = {}
            for (x, y) in self.tornadoes[self.step-1]:
                for (dx, dy) in self.tornadoes[self.step-1][(x, y)]:
                    tx = dx + x
                    ty = dy + y
                    if tx == 0:
                        tx += self.dimensions[0] - 2
                    if tx == self.dimensions[0] - 1:
                        tx -= self.dimensions[0] - 2
                    if ty == 0:
                        ty += self.dimensions[1] - 2
                    if ty == self.dimensions[1] - 1:
                        ty -= self.dimensions[1] - 2
                    if (tx, ty) not in new_ts:
                        new_ts[(tx, ty)] = []
                    new_ts[(tx, ty)].append((dx, dy))
            self.tornadoes[self.step] = new_ts
        new_moves = []
        for mx, my in [(-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)]:
            mx += self.position[0]
            my += self.position[1]
            if (mx, my) == self.exit:
                if not adv or self.state == 2:
                    self.position = (mx, my)
                    return True, self
            if (0 < mx < self.dimensions[0] - 1 and 0 < my < self.dimensions[1] - 1) or ((mx, my) == self.start) or ((mx, my) == self.exit):
                if (mx, my) not in self.tornadoes[self.step]:
                    new_m = Map(o=self)
                    new_m.position = (mx, my)
                    if adv and (((mx, my) == self.start and self.state == 1) or ((mx, my) == self.exit and self.state == 0)):
                        new_m.state += 1
                    new_moves.append(new_m)
        return False, new_moves

    def __str__(self):
        map = ''
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                if (x, y) == self.position:
                    map += 'X'
                elif x == 0 or y == 0 or x == self.dimensions[0] - 1 or y == self.dimensions[1] - 1:
                    map += '#'
                else:
                    map += '@' if (x,y) in self.tornadoes[self.step] and len(self.tornadoes[self.step][(x,y)]) > 0 else '.'
            map += '\n'
        return map


def run(map, adv=False):
    buffer = [map]
    i = 0
    while len(buffer) > 0:
        i += 1
        if i % 10000 == 0:
            print(F"Buffer has {len(buffer)} items @ {buffer[0].step} minutes.")
        m = buffer.pop(0)
        res, moves = m.turn(adv)
        if res:
            print(moves)
            return moves.step
        for m in moves:
            if m not in buffer:
                buffer.append(m)
    return None


assert run(Map(common.Loader.load_lines('test_s'))) == 10
assert run(Map(common.Loader.load_lines('test'))) == 18
print(f"Minimum minutes is {run(Map(common.Loader.load_lines()))}")


assert run(Map(common.Loader.load_lines('test_s')), True) == 30
assert run(Map(common.Loader.load_lines('test')), True) == 54
print(f"Minimum minutes is {run(Map(common.Loader.load_lines()), True)}")