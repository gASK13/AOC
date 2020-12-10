class Unit:
    def __init__(self, char, x, y):
        self.x = x
        self.y = y
        self.attack = 3
        if char == 'E':
            self.attack = 19
        self.hp = 200
        self.elf = char == 'E' 
        self.char = char
    def __str__(self):
        return self.char + "@" + str(self.x) + ":" + str(self.y) + " (" + str(self.hp) + ") !" + str(self.attack)
    def __repr__(self):
        return self.char + "@" + str(self.x) + ":" + str(self.y) + " (" + str(self.hp) + ") !" + str(self.attack)
    def noEnemies(self, units):
        for u in units:
            if (u.hp > 0) & (u.elf != self.elf):
                return False
        return True
    def enemiesInRange(self, units):
        retunits = []
        for u in units:
            if u.hp <= 0:
                continue
            if u.elf == self.elf:
                continue
            if (abs(u.x - self.x) + abs(u.y - self.y)) <= 1:
                 retunits.append(u)
        return retunits
    def stab(self, unit, map):
        unit.hp -= self.attack
        if unit.hp <= 0:
            map[unit.x] = map[unit.x][0:unit.y] + '.' + map[unit.x][unit.y+1:len(map[unit.x])]
    def squares(self, map):
        sq = []
        if map[self.x-1][self.y] == '.': sq.append(Square(self.x-1, self.y))
        if map[self.x+1][self.y] == '.': sq.append(Square(self.x+1, self.y))
        if map[self.x][self.y-1] == '.': sq.append(Square(self.x, self.y-1))
        if map[self.x][self.y+1] == '.': sq.append(Square(self.x, self.y+1))
        return sq
    def allSquares(self, units, map):
        sqa = []
        for unit in units:
            if unit.hp <= 0:
                continue
            if unit.elf == self.elf:
                continue
            sqa.extend(unit.squares(map))
        return sqa
    def move(self, sq, map):
        newc = sq.path.path[0]
        newy = newc % 1000
        newx = int((newc - newy) / 1000)
        map[self.x] = map[self.x][0:self.y] + '.' + map[self.x][self.y+1:len(map[self.x])]
        self.x = newx
        self.y = newy
        map[self.x] = map[self.x][0:self.y] + self.char + map[self.x][self.y+1:len(map[self.x])]

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = None
    def __str__(self):
        return str(self.x) + ":" + str(self.y)
    def __repr__(self):
        return str(self.x) + ":" + str(self.y)

class Path:
    def __init__(self, path, sq, distance):
        self.path = []
        self.path.extend(path)
        self.path.append(sq)
        self.distance = distance
    def last(self):
        return self.path[len(self.path) - 1]

def distance(sq, unit, map):
    u = unit.x * 1000 + unit.y
    visited = [u + 1, u - 1, u + 1000, u - 1000]
    current = []
    next = [Path([], u - 1000, 1), Path([], u - 1, 1), Path([], u + 1, 1), Path([], u + 1000, 1)]
    goal = sq.x * 1000 + sq.y
    while len(next) > 0:
        current = next
        next = []
        while len(current) > 0:
            ci = current.pop(0)
            c = ci.last()
            cy = c % 1000
            cx = int((c - cy) / 1000)
            if (cx >= len(map)) | (cy >= len(map[0])) | (cx < 0) | (cy < 0):
                continue
            if map[cx][cy] != '.':
                continue
            if c == goal:
                return ci
            if (c + 1) not in visited:
                visited.append(c+1)
                next.append(Path(ci.path, c + 1, ci.distance + 1))
            if (c - 1) not in visited:
                visited.append(c-1)
                next.append(Path(ci.path, c - 1, ci.distance + 1))
            if (c + 1000) not in visited:
                visited.append(c+1000)
                next.append(Path(ci.path, c + 1000, ci.distance + 1))
            if (c - 1000) not in visited:
                visited.append(c-1000)
                next.append(Path(ci.path, c - 1000, ci.distance + 1))
    return None

def unitOrder(cart):
    return cart.x * 1000 + cart.y

def distOrder(sq):
    return sq.path.distance * 1000000 + sq.x * 1000 + sq.y

def hpOrder(unit):
    return unit.hp * 1000000 + unit.x * 1000 + unit.y

def isUnit(char):
    return (char == 'E') | (char == 'G')

def getUnits(line, x):
    carts = []
    line = line.rstrip()
    for y in range(len(line)):
        if(isUnit(line[y])):
            carts.append(Unit(line[y], x, y))    
    return carts

def printMap(map, carts):
    for line in map:
        print(line)
    print('')
    for unit in carts:
        print(unit)
    print('')

map = []
units = []
x = 0
for line in open('combat.txt', 'r').readlines():
    map.append(line.rstrip())
    units.extend(getUnits(line, x))
    x += 1

print(0)
printMap(map, units)

combat = True
rounds = 0
while combat:
    units.sort(key=unitOrder)
    for unit in units:
        if unit.hp <= 0:
            continue
        if unit.noEnemies(units):
            combat = False
            break;            
        eir = unit.enemiesInRange(units)
        if len(eir) > 0:
            eir.sort(key=hpOrder)
            unit.stab(eir[0], map)
            continue
        sqs = unit.allSquares(units,map)
        for sq in sqs:
            sq.path = distance(sq, unit, map)
        sqs = list(filter(lambda s : s.path != None, sqs))
        sqs.sort(key=distOrder)
        if len(sqs) > 0:
            unit.move(sqs[0], map)
            eir = unit.enemiesInRange(units)
            if len(eir) > 0:
                eir.sort(key=hpOrder)
                unit.stab(eir[0], map)
                continue
    if combat:
        rounds += 1
    print(rounds)
    printMap(map, units)
    if len(list(filter(lambda u : (u.hp <= 0) & (u.elf), units))) > 0:
        print("DEAD ELF, DEAD ELF!")
        break
    units = list(filter(lambda u : u.hp > 0, units))

tot = 0
for unit in units:
    tot += unit.hp

print(str(rounds) + "*" + str(tot) + "=" + str(tot*rounds))