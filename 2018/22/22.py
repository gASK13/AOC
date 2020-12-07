import copy
import operator

def printMap(mat):
    for line in mat:
        print(''.join([str(item) for item in line]))

class Status:
    def __init__(self, x, y, tool, time):
        self.x = x
        self.y = y
        self.tool = tool
        self.time = time

class Region:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.geo = 0
        self.ero = 0
        self.target = False
        self.time = {'C': 999999999, 'T':999999999, 'N':999999999}
    def __str__(self):
        return self.typeStr()
    def setGeo(self, geo, depth):
        self.geo = geo
        self.ero = (geo + depth) % 20183
    def typeRisk(self):
        return self.ero % 3
    def typeStr(self):
        if self.typeRisk() == 0:
            return '.'
        if self.typeRisk() == 1:
            return '='
        if self.typeRisk() == 2:
            return '|'
    def validTools(self):
        if self.typeRisk() == 0:
            return ['C', 'T']
        if self.typeRisk() == 1:
            return ['C', 'N']
        if self.typeRisk() == 2:
            return ['N', 'T']
    def otherTool(self, tool):
        tls = self.validTools()
        tls.remove(tool)
        if len(tls) > 1:
            raise Exception('OOPS!')
        return tls[0]
    def checkTool(self, tool):
        return tool in self.validTools()

def computeMap(map, depth, target):
    for (row, line) in enumerate(map):
        for (col, region) in enumerate(line):
            if (row == 0) & (col == 0):
                region.setGeo(0, depth)
            elif (row == target['y']) & (col == target['x']):
                region.setGeo(0, depth)
                region.target = True
            elif (row == 0):
                region.setGeo(col * 16807, depth)
            elif (col == 0):
                region.setGeo(row * 48271, depth)
            else:
                region.setGeo(map[row][col - 1].ero * map[row - 1][col].ero, depth)

def computeRisk(map, target):
    risk = 0
    for line in range(0, target['y'] + 1):
        for region in range(0, target['x'] + 1):
            risk += map[line][region].typeRisk()
    return risk


#target = {'x' : 10, 'y' : 10}
#depth = 510

target = {'x' : 13, 'y' : 726}
depth = 3066

# this is "trial and error constant" to get map "just large enough"
factor = 4

map = [[Region(x, y) for x in range(0, target['x'] * factor)] for y in range(0, target['y'] * factor)]
computeMap(map, depth, target)

print('Total risk is {}'.format(computeRisk(map, target)))

stack = [Status(0, 0, 'T', 0)]
directions = [[0, -1], [-1, 0], [0, 1], [1, 0]]
trgtRegion = map[target['y']][target['x']]

while len(stack) > 0:
    stack.sort(key=operator.attrgetter('time'), reverse=True)
    curr = stack.pop()
    #print('At {}:{} in time {} (stack size is {}).'.format(curr.x, curr.y, curr.time, len(stack)))
    if curr.time > trgtRegion.time['T']:
        print(trgtRegion.time['T'])
        break
    region = map[curr.y][curr.x]
    if region.time[curr.tool] > curr.time:
        region.time[curr.tool] = curr.time
        region.time[region.otherTool(curr.tool)] = curr.time + 7
        for dir in directions:
            dx = curr.x + dir[0]
            dy = curr.y + dir[1]
            if (dx >= 0) & (dx < len(map[0])) & (dy >= 0) & (dy < len(map)):
                if (map[dy][dx].checkTool(curr.tool)) & (map[dy][dx].time[curr.tool] > curr.time + 1):
                    stack.append(Status(dx, dy, curr.tool, curr.time + 1))
                elif (map[dy][dx].checkTool(region.otherTool(curr.tool))) & (map[dy][dx].time[region.otherTool(curr.tool)] > curr.time + 8):
                    stack.append(Status(dx, dy, region.otherTool(curr.tool), curr.time + 8))
