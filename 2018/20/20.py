import copy
import re

class Cell:
    def __init__(self, map, x, y):
        self.east = None
        self.west = None
        self.north = None
        self.south = None
        self.x = x
        self.y = y
        self.map = map
        self.distance = None
    def join(self, char):
        if char == 'E':
            joinCell = self.map.get(self.x + 1, self.y)
            joinCell.west = self
            self.east = joinCell
        if char == 'W':
            joinCell = self.map.get(self.x - 1, self.y)
            joinCell.east = self
            self.west = joinCell
        if char == 'S':
            joinCell = self.map.get(self.x, self.y + 1)
            joinCell.north = self
            self.south = joinCell
        if char == 'N':
            joinCell = self.map.get(self.x, self.y - 1)
            joinCell.south = self
            self.north = joinCell
        return joinCell
    def id(self):
        return self.y * 10000 + self.x
    def propagateDistance(self):
        next = []
        if self.east is not None:
            if not self.east.distance:
                self.east.distance = self.distance + 1
                next.append(self.east)
        if self.west is not None:
            if not self.west.distance:
                self.west.distance = self.distance + 1
                next.append(self.west)
        if self.north is not None:
            if not self.north.distance:
                self.north.distance = self.distance + 1
                next.append(self.north)
        if self.south is not None:
            if not self.south.distance:
                self.south.distance = self.distance + 1
                next.append(self.south)
        return next


class Map:
    def __init__(self):
        self.map = {}
    def get(self, x, y):
        id = self.id(x, y)
        if id not in self.map:
            self.map[id] = Cell(self, x, y)
        return self.map[id]
    def id(self, x, y):
        return y * 10000 + x
    def computeDistances(self):
        cell = self.get(0, 0)
        cell.distance = 0
        stack = [cell]
        while len(stack) > 0:
            c = stack.pop()
            stack += c.propagateDistance()
    def getMaxDistance(self):
        max = 0
        for cell in self.map.values():
            if cell.distance > max:
                max = cell.distance
        return max
    def getCountByDistance(self, min):
        max = 0
        for cell in self.map.values():
            if cell.distance >= min:
                max += 1
        return max

def checkEnds(curr, ends):
    id = curr.id()
    different = []
    for end in ends:
        if id != end.id():
            #print('NOT MATCHING: ' + str(id) + '/' + str(end.id()))
            different.append(end)
    return different

def buildMap(line):
    map = Map()
    cell = map.get(0, 0)
    branches = [{ 'p' : 1, 'stack' : [], 'cell' : cell}]
    while len(branches) > 0:
        branch = branches.pop()
        p = branch['p']
        cell = branch['cell']
        stack = branch['stack']
        print("Starting branch: " + line[p:])
        print(stack)
        while line[p] != '$':
            if re.match('[ENWS]', line[p]):
                cell = cell.join(line[p])
            if line[p] == '(':
                stack.append({'cell': cell, 'ends': []})
            if line[p] == '|':
                curr = stack.pop()
                curr['ends'].append(cell)
                cell = curr['cell']
                stack.append(curr)
            if line[p] == ')':
                curr = stack.pop()
                ends = checkEnds(cell, curr['ends'])
                for end in ends:
                    if not re.match('\)*\$', line[p + 1:]):
                        if (line[p + 1] == '|') | (line[p + 1] == ')'):
                            nextCur = stack.pop()
                            nextCur['ends'].append(end)
                            stack.append(nextCur)
                        else:
                            print(line[p:])
                            branches.append({ 'p' : p + 1, 'stack' : copy.deepcopy(stack), 'cell' : end})
            p += 1

    return map

#23
#map = buildMap("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")


#31
#map = buildMap("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")


for line in open('input.txt', 'r').readlines():
    map = buildMap(line)

map.computeDistances()
print(map.getMaxDistance())
print(map.getCountByDistance(1000))
