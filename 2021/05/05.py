import common


class VentLine:
    def __init__(self, line):
        points = line.split(' -> ')
        self.start = [int(x) for x in points[0].split(',')]
        self.end = [int(x) for x in points[1].split(',')]

    def get_points(self):
        step = (0,0)
        len = 0
        if self.start[1] != self.end[1]:
            step = (step[0], 1 if self.start[1] < self.end[1] else -1)
            len = abs(self.start[1] - self.end[1]) + 1
        if self.end[0] != self.start[0]:
            step = (1 if self.start[0] < self.end[0] else -1, step[1])
            len = abs(self.start[0] - self.end[0]) + 1
        return [(self.start[0] + step[0] * i, self.start[1] + step[1] * i) for i in range(len)]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{}, {} -> {}, {}".format(self.start[0], self.start[1], self.end[0], self.end[1])


#vents = common.Loader.transform_lines(VentLine, filename='test.txt')
vents = common.Loader.transform_lines(VentLine)
heatmap = {}
for v in vents:
    print(v)
    for point in v.get_points():
        hash = common.hash_list(point)
        if hash not in heatmap:
            heatmap[hash] = 0
        heatmap[hash] += 1

print(sum([1 for h in heatmap if heatmap[h] > 1]))
