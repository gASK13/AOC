import common
import hashlib


class MazeState:
    def __init__(self, code, path, x, y):
        self.code = code
        self.path = path
        self.x = x
        self.y = y
        self.hash = hashlib.md5(f'{self.code}{self.path}'.encode('utf-8')).hexdigest()

    def win(self):
        if self.x == 4 and self.y == 4:
            return True
        return False

    def moves(self):
        dirs = [(0, -1, 'U'), (0, 1, 'D'), (-1, 0, 'L'), (1, 0, 'R')]
        moves = []
        for i in range(4):
            if self.hash[i] in 'bcdef' and 0 < self.x + dirs[i][0] <= 4 and 0 < self.y + dirs[i][1] <= 4:
                moves.append(MazeState(self.code, self.path + dirs[i][2], self.x + dirs[i][0], self.y + dirs[i][1]))
        return moves


def find_shortest(code):
    buffer = [MazeState(code, '', 1, 1)]
    while len(buffer) > 0:
        state = buffer.pop(0)
        if state.win():
            return state.path
        buffer += state.moves()


def find_longest(code):
    buffer = [MazeState(code, '', 1, 1)]
    longest = buffer[0]
    while len(buffer) > 0:
        state = buffer.pop(0)
        if state.win():
            longest = state
        else:
            buffer += state.moves()
    return len(longest.path)


assert find_shortest('ihgpwlah') == 'DDRRRD'
assert find_shortest('kglvqrro') == 'DDUDRLRRUDRD'
assert find_shortest('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
print(f'Shortest path for input is {find_shortest(common.Loader.load_lines()[0])}')

assert find_longest('ihgpwlah') == 370
assert find_longest('kglvqrro') == 492
assert find_longest('ulqzkmiv') == 830
print(f'Longest path for input is {find_longest(common.Loader.load_lines()[0])}')