class Vein:
    def __init__(self, line):
        for part in line.split(', '):
            nums = part.split('=')[1].split('..')
            if part.split('=')[0] == 'x':
                self.minx = int(nums[0])
                self.maxx = int(nums[1]) if len(nums) > 1 else int(nums[0])
            else:
                self.miny = int(nums[0])
                self.maxy = int(nums[1]) if len(nums) > 1 else int(nums[0])
    def normalize(self, minx, miny):
        self.minx -= minx
        self.miny -= miny
        self.maxx -= minx
        self.maxy -= miny
    def apply(self, map):
        for x in range(self.minx, self.maxx + 1):
            for y in range(self.miny, self.maxy + 1):
                map[y][x] = '#'

def printmap(map):
    for line in map:
        print(''.join(line))

def flow(map, x, y):
    cy = y
    if map[y][x] == '~':
        return None
    while True:
        if cy >= len(map):
            return None
        if map[cy][x] == '.':
            map[cy][x] = '|'
            cy += 1
        elif map[cy][x] == '|':
            return None
        elif (map[cy][x] == '~') | (map[cy][x] == '#') :
            return cy - 1
        else:
            map[cy][x] = 'O'
            print('WTF')
            printmap(map)
            x = [0][2]

def fill(map, x, y):
    cy = y
    while True:
        map[cy][x] = '~'
        lx = x - 1
        while ((map[cy][lx] == '.') | (map[cy][lx] == '|')) & ((map[cy + 1][lx] == '#') | (map[cy + 1][lx] == '~')):
            map[cy][lx] = '~'
            lx -= 1
        rx = x + 1
        while ((map[cy][rx] == '.') | (map[cy][rx] == '|')) & ((map[cy + 1][rx] == '#') | (map[cy + 1][rx] == '~')):
            map[cy][rx] = '~'
            rx += 1
        if (map[cy][rx] == '.') | (map[cy][lx] == '.') | (map[cy][rx] == '|') | (map[cy][lx] == '|'):
            retval = []
            for ex in range(lx + 1, rx):
                map[cy][ex] = '|'
            if map[cy][rx] == '.':
                retval.append([rx, cy])
            if map[cy][lx] == '.':
                retval.append([lx, cy])
            return retval
        else:
            cy -= 1

veins = []
minx = 501
maxx = 499
miny = 99999
maxy = 0
for line in open('17.txt', 'r').readlines():
    v = Vein(line)
    veins.append(v)
    if v.minx < minx:
        minx = v.minx
    if v.maxx > maxx:
        maxx = v.maxx
    if v.maxy > maxy:
        maxy = v.maxy
    if v.miny < miny:
        miny = v.miny

minx -= 1
maxx += 1
miny -= 1

source = 500 - minx

map = [['.'] * (maxx - minx + 1) for _ in range(maxy - miny + 1)]

for vein in veins:
    vein.normalize(minx, miny)
    vein.apply(map)

map[0][source] = '+'
flowbuffer = [[source, 1]]
while len(flowbuffer) > 0:
    next = flowbuffer.pop()
    fill_new = flow(map, next[0], next[1])
    if fill_new:
        for x in fill(map, next[0], fill_new):
            flowbuffer.append(x)

printmap(map)

cnt = 0
cnt_rest = 0
for line in map:
    for item in line:
        if (item == '~') | (item == '|'):
            cnt += 1
        if (item == '~'):
            cnt_rest += 1

print(cnt)
print(cnt_rest)