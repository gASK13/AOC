import operator
import re

class Nanobot:
    def __init__(self, line):
        parsed = re.findall('(-?[0-9]+)', line.strip())
        self.x = int(parsed[0])
        self.y = int(parsed[1])
        self.z = int(parsed[2])
        self.radius = int(parsed[3])
        self.outrange = set()

    def __str__(self):
        return '<{}:{}:{}>, radius {}, count {}'.format(self.x, self.y, self.z, self.radius, self.count())

    def connect(self, other):
        distance = abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
        if self.radius >= distance:
            self.outrange.add(other)
        if other.radius >= distance:
            other.outrange.add(self)

    def isInRange(self, x, y, z):
        distance = abs(self.x - x) + abs(self.y - y) + abs(self.z - z)
        return distance <= self.radius

    def count(self):
        return len(self.outrange)


class Cube:
    def __init__(self, x, y, z, size, bots):
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.neg_distance = - abs(self.x) - abs(self.y) - abs(self.z)
        self.count = 0
        for bot in bots:
            if self.overlaps(bot):
                self.count += 1

    def overlaps(self, bot):
        xOverlaps = (self.x <= bot.x <= self.x + self.size)
        yOverlaps = (self.y <= bot.y <= self.y + self.size)
        zOverlaps = (self.z <= bot.z <= self.z + self.size)
        if (xOverlaps & yOverlaps & zOverlaps) |\
                (xOverlaps & yOverlaps & bot.isInRange(bot.x, bot.y, self.z)) | (xOverlaps & yOverlaps & bot.isInRange(bot.x, bot.y, self.z + self.size)) |\
                (xOverlaps & zOverlaps & bot.isInRange(bot.x, self.y, bot.z)) | (xOverlaps & zOverlaps & bot.isInRange(bot.x, self.y + self.size, bot.z)) |\
                (yOverlaps & zOverlaps & bot.isInRange(self.x, bot.y, bot.z)) | (yOverlaps & zOverlaps & bot.isInRange(self.x + self.size, bot.y, bot.z)) |\
                (xOverlaps & bot.isInRange(bot.x, self.y, self.z)) | (xOverlaps & bot.isInRange(bot.x, self.y + self.size, self.z)) | \
                (xOverlaps & bot.isInRange(bot.x, self.y, self.z + self.size)) | (xOverlaps & bot.isInRange(bot.x, self.y + self.size, self.z + self.size)) | \
                (yOverlaps & bot.isInRange(self.x, bot.y, self.z)) | (yOverlaps & bot.isInRange(self.x + self.size, bot.y, self.z)) | \
                (yOverlaps & bot.isInRange(self.x, bot.y, self.z + self.size)) | (yOverlaps & bot.isInRange(self.x + self.size, bot.y, self.z + self.size)) | \
                (zOverlaps & bot.isInRange(self.x, self.y, bot.z)) | (zOverlaps & bot.isInRange(self.x + self.size, self.y, bot.z)) | \
                (zOverlaps & bot.isInRange(self.x, self.y + self.size, bot.z)) | (zOverlaps & bot.isInRange(self.x + self.size, self.y + self.size, bot.z)) | \
                (bot.isInRange(self.x, self.y, self.z)) | (bot.isInRange(self.x, self.y, self.z + self.size)) | \
                (bot.isInRange(self.x, self.y + self.size, self.z)) | (bot.isInRange(self.x + self.size, self.y, self.z)) |\
                (bot.isInRange(self.x + self.size, self.y + self.size, self.z)) | (bot.isInRange(self.x + self.size, self.y, self.z + self.size)) |\
                (bot.isInRange(self.x, self.y + self.size, self.z + self.size)) | (bot.isInRange(self.x + self.size, self.y + self.size, self.z + self.size)):
            return True
        return False

    def split(self, bots):
        newSize = int(self.size / 2)
        return [Cube(self.x + newSize, self.y, self.z, newSize, bots), Cube(self.x, self.y + newSize, self.z, newSize, bots), Cube(self.x, self.y, self.z + newSize, newSize, bots),
                Cube(self.x + newSize, self.y + newSize, self.z, newSize, bots), Cube(self.x, self.y + newSize, self.z + newSize, newSize, bots), Cube(self.x + newSize, self.y, self.z + newSize, newSize, bots),
                Cube(self.x, self.y, self.z, newSize, bots), Cube(self.x + newSize, self.y + newSize, self.z + newSize, newSize, bots)]

    def __str__(self):
        return '{}:{}:{}@{} - in range: {}, distance: {}'.format(self.x, self.y, self.z, self.size, self.count, -self.neg_distance)

nanobots = []
for line in open('23.txt', 'r').readlines():
    nanobots.append(Nanobot(line))

# Part ONE
for i in range(0, len(nanobots)):
    for j in range(i, len(nanobots)):
        nanobots[i].connect(nanobots[j])

nanobots.sort(key=operator.methodcaller('count'))
print(str(nanobots[-1]))

# constant 2^X
# I don't count negative coords since my solution is "skewed" towards positive ones
size = 268435456
stack = [Cube(0, 0, 0, size, nanobots)]
while len(stack) > 0:
    stack.sort(key=operator.attrgetter('count', 'neg_distance'))
    cube = stack.pop()
    print(str(cube))
    if cube.size == 0:
        print("--------- END ----------")
        print(str(cube))
        break
    stack += cube.split(nanobots)
