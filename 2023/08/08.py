import common

class Game:

    def __init__(self, lines, ghost=False):
        self.moves = [0 if c == 'L' else 1 for c in lines[0]]
        self.map = {}
        for line in lines[2:]:
            self.map[line.split(' = ')[0]] = line.split(' = ')[1][1:-1].split(', ')
        self._move = 0
        self._pos = ['AAA'] if not ghost else [_ for _ in self.map if _[-1] == 'A']
        self._steps = 0
        self._cycles = []

    def step(self):
        self._steps += 1
        for i in range(len(self._pos)):
            self._pos[i] = self.map[self._pos[i]][self.moves[self._move]]
        self._move += 1
        self._move %= len(self.moves)

    def reach(self, goal_suffix):
        while True:
            for pos in self._pos:
                if pos.endswith(goal_suffix):
                    self._pos.remove(pos)
                    self._cycles.append(self._steps)

            if len(self._pos) == 0:
                # find lowest common multiple of cycles
                lcm = self._cycles[0]
                for i in self._cycles[1:]:
                    lcm = lcm * i // common.gcd(lcm, i)
                return lcm

            self.step()


assert Game(common.Loader.load_lines('test')).reach('ZZZ') == 2
assert Game(common.Loader.load_lines('test2')).reach('ZZZ') == 6

print(f'Part 1: {Game(common.Loader.load_lines()).reach("ZZZ")}')

assert Game(common.Loader.load_lines('test_p2'), True).reach('Z') == 6

print(f'Part 2: {Game(common.Loader.load_lines(), True).reach("Z")}')