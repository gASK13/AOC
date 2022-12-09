import common


class Map:
    def __init__(self, input):
        self.input = input

    def is_wall(self, x, y):
        value = x*x + 3*x + 2*x*y + y + y*y + self.input
        return bin(value).count('1') % 2 == 1


def find_path(input, goal_x=None, goal_y=None):
    m = Map(input)
    visited = {'1#1': 0}
    buffer = [(1, 1, 0)]
    while len(buffer) > 0:
        (x, y, ln) = buffer.pop(0)
        if x == goal_x and y == goal_y:
            return ln
        if goal_x is None and ln == 51:
            print(visited)
            return sum([1 for v in visited.values() if 0 <= v < 51])
        for (dx, dy) in [(x + 1, y + 0), (x + -1, y + 0), (x + 0, y + 1), (x + 0, y + -1)]:
            if dx >= 0 and dy >= 0:
                if f'{dx}#{dy}' not in visited:
                    if not m.is_wall(dx, dy):
                        visited[f'{dx}#{dy}'] = ln + 1
                        buffer.append((dx, dy, ln + 1))
                    else:
                        visited[f'{dx}#{dy}'] = -1
    return -213


assert not Map(10).is_wall(0, 0)
assert not Map(10).is_wall(7, 2)
assert not Map(10).is_wall(6, 4)
assert not Map(10).is_wall(2, 6)
assert not Map(10).is_wall(3, 6)
assert Map(10).is_wall(1, 0)
assert Map(10).is_wall(9, 1)
assert Map(10).is_wall(0, 3)
assert Map(10).is_wall(1, 4)
assert Map(10).is_wall(5, 6)

assert find_path(10, 7, 4) == 11
print(find_path(int(common.loader.Loader.load_lines()[0]), 31, 39))
print(find_path(int(common.loader.Loader.load_lines()[0])))

