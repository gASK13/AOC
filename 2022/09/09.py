import common
import operator


class Snake:
    def __init__(self, length = 1):
        self.snake = [[0, 0] for i in range(length + 1)]
        self.visited = set()
        self.visited.add(common.utils.hash_list(self.snake[-1]))

    def move(self, direction, distance=1):
        directions = {'U' : (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
        for i in range(distance):
            self.snake[0] = list(map(operator.add, self.snake[0], directions[direction]))
            self.pull_tail()

    def pull_tail(self):
        for i in range(1, len(self.snake)):
            if abs(self.snake[i-1][0] - self.snake[i][0]) > 1 and abs(self.snake[i-1][1] - self.snake[i][1]) > 1:
                self.snake[i] = list(map(operator.add, self.snake[i], (1 if self.snake[i-1][0] > self.snake[i][0] else -1, 1 if self.snake[i-1][1] > self.snake[i][1] else -1)))
            elif abs(self.snake[i-1][0] - self.snake[i][0]) > 1:
                self.snake[i] = list(map(operator.add, self.snake[i], (1 if self.snake[i-1][0] > self.snake[i][0] else -1, self.snake[i-1][1] - self.snake[i][1])))
            elif abs(self.snake[i-1][1] - self.snake[i][1]) > 1:
                self.snake[i] = list(map(operator.add, self.snake[i], (self.snake[i-1][0] - self.snake[i][0], 1 if self.snake[i-1][1] > self.snake[i][1] else -1)))

        self.visited.add(common.utils.hash_list(self.snake[-1]))


def run_snake(lines, length=1):
    s = Snake(length)
    for line in lines:
        (direction, size) = line.split(' ')
        s.move(direction, int(size))
    return s.visited


assert len(run_snake(common.Loader.load_lines('test'))) == 13
print(f'Snake tail has visited {len(run_snake(common.Loader.load_lines()))} locations.')

assert len(run_snake(common.Loader.load_lines('test'), 9)) == 1
assert len(run_snake(common.Loader.load_lines('test_l'), 9)) == 36
print(f'Long snake tail has visited {len(run_snake(common.Loader.load_lines(), 9))} locations.')
