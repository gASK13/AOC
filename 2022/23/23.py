import common
from collections import Counter

class Map:
    def __init__(self, lines):
        self.elves = set()
        self.no_turn = 0
        self._rules = [{"rule": [(0, -1), (-1, -1), (1, -1)], "move": (0, -1)},
             {"rule": [(0, 1), (-1, 1), (1, 1)], "move": (0, 1)},
             {"rule": [(-1, 0), (-1, -1), (-1, 1)], "move": (-1, 0)},
             {"rule": [(1, 0), (1, -1), (1, 1)], "move": (1, 0)}]
        for (y, line) in enumerate(lines):
            for (x, char) in enumerate(line):
                if char == '#':
                    self.elves.add((x, y))

    def __repr__(self):
        return f'EMAP {len(self.elves)}'

    def turn(self):
        self.no_turn += 1
        moves = {}
        for x, y in self.elves:
            if all([(x+rx, y+ry) not in self.elves for rx, ry in [(-1, 0), (-1, -1), (-1, 1), (1, 0), (1, -1), (1, 1), (0, -1), (0, 1)]]):
                continue
            for rule in self._rules:
                if all([(x+rx, y+ry) not in self.elves for rx, ry in rule["rule"]]):
                    nx = x + rule["move"][0]
                    ny = y + rule["move"][1]
                    if (nx, ny) not in moves:
                        moves[(nx, ny)] = []
                    moves[(nx, ny)].append((x, y))
                    break
        valid_moves = [m for m in moves if len(moves[m]) == 1]
        for i in valid_moves:
            self.elves.remove(moves[i][0])
            self.elves.add(i)
        self._rules.append(self._rules.pop(0))
        return len(valid_moves) > 0

    def __str__(self):
        map = ''
        for y in range(sorted([y for x, y in self.elves])[0], sorted([y for x, y in self.elves])[-1] + 1):
            for x in range(sorted([x for x, y in self.elves])[0], sorted([x for x, y in self.elves])[-1] + 1):
                map += '#' if (x,y) in self.elves else '.'
            map += '\n'
        return map


m = Map(common.Loader.load_lines('test_small'))
while m.turn():
    pass
assert str(m) == '..#..\n....#\n#....\n....#\n.....\n..#..\n'

m = Map(common.Loader.load_lines('test'))
for i in range(10):
    m.turn()
assert Counter(str(m))['.'] == 110
while m.turn():
    pass
assert m.no_turn == 20

m = Map(common.Loader.load_lines())
for i in range(10):
    m.turn()
print(f"Empty tiles count after turn 10 - {Counter(str(m))['.']}")
while m.turn():
    pass
print(f"Finished after {m.no_turn} turns.")
