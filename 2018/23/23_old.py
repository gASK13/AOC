import operator
import re

class Nanobot:
    def __init__(self, line):
        parsed = re.findall('(-?[0-9]+)', line.strip())
        self.x = int(parsed[0])
        self.y = int(parsed[1])
        self.z = int(parsed[2])
        self.radius = int(parsed[3])
        self.inrange = set()
        self.outrange = set()

    def __str__(self):
        return '<{}:{}:{}>, radius {}, count {}, incount {}'.format(self.x, self.y, self.z, self.radius, self.count(), self.inrangecount())

    def connect(self, other):
        distance = abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
        if self.radius >= distance:
            self.outrange.add(other)
            other.inrange.add(self)
        if other.radius >= distance:
            other.outrange.add(self)
            self.inrange.add(other)

    def isInRange(self, x, y, z):
        distance = abs(self.x - x) + abs(self.y - y) + abs(self.z - z)
        return distance <= self.radius

    def count(self):
        return len(self.outrange)

    def inrangecount(self):
        return len(self.inrange)

class Result:
    def __init__(self, x, y, z, bots):
        self.x = x
        self.y = y
        self.z = z
        self.count = 0
        self.dist = abs(self.x) + abs(self.y) + abs(self.z)
        self.inversedist = 1000000000 - self.dist
        for bot in bots:
            if bot.isInRange(x, y, z):
                self.count = self.count + 1

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __str__(self):
        return "{}:{}:{} @ {} - {}".format(self.x, self.y, self.z, self.dist, self.count)


def computeHeatMap(bots, sx, ex, sy, ey, sz, ez, resolution):
    print('{}:{} / {}:{} / {}:{} / {}'.format(sx, ex, sy, ey, sz, ez, resolution))
    result = []
    for z in range(sz, ez+1, resolution):
        for y in range(sy, ey+1, resolution):
            for x in range(sx, ex+1, resolution):
                result.append(Result(x, y, z, bots))
    return result


nanobots = []
for line in open('23.txt', 'r').readlines():
    nanobots.append(Nanobot(line))

for i in range(0, len(nanobots)):
    for j in range(i, len(nanobots)):
        nanobots[i].connect(nanobots[j])

nanobots.sort(key=operator.methodcaller('inrangecount'))
print(str(nanobots[-1]))

#13839482:58667777:26690000 @ 99197259 - 935

sx = 13839482
ex = 13839482
sy = 58667000
ey = 58669800
sz = 26690000
ez = 26692000
valid = []
for bot in nanobots:
    if (bot.isInRange(sx,sy,sz)) | (bot.isInRange(sx,sy,ez)) | (bot.isInRange(sx,ey,sz)) | (bot.isInRange(ex,sy,sz))\
            & (bot.isInRange(ex,ey,sz)) | (bot.isInRange(ex,sy,ez)) | (bot.isInRange(sx,ey,ez)) | (bot.isInRange(ex,ey,ez)):
        valid.append(bot)

print(len(valid))
res = computeHeatMap(nanobots, sx, ex, sy, ey, sz, ez, 1)

res.sort(key=operator.attrgetter("count", "inversedist"))
br = res.pop()
print(str(br))