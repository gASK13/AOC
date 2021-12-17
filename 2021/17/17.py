import common


class Target:
    def __init__(self, line):
        self.min_x, self.max_x = [int(s) for s in line.split(',')[0].split('x=')[1].split('..')]
        self.min_y, self.max_y = [int(s) for s in line.split(',')[1].split('y=')[1].split('..')]

    def hit(self, x, y):
        return self.min_y <= y <= self.max_y and self.min_x <= x <= self.max_x

    def is_out(self, x, y):
        return x > self.max_x or y < self.min_y


def max_height(dx, dy, target):
    x = dx
    y = dy
    sx = 0
    sy = 0
    maxy = 0
    while not target.is_out(sx, sy):
        sx += x
        sy += y
        if sy > maxy:
            maxy = sy
        if x != 0:
            x -= 1 if x >= 0 else -1
        y -= 1
        if target.hit(sx, sy):
            return maxy
    return -1000  # default


test_target = Target('target area: x=20..30, y=-10..-5')
data = [max_height(x, y, test_target) for x in range(test_target.max_x + 1) for y in range(test_target.min_y, 1000)]
print(f'Test = {max(data)} / {len([d for d in data if d > -1000])} expected 45 / 112.')

target = common.Loader.transform_lines(Target)[0]
data = [max_height(x, y, target) for x in range(target.max_x + 1) for y in range(target.min_y, 1000)]
print(f'Real = {max(data)} / {len([d for d in data if d > -1000])}')
