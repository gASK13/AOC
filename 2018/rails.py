def parseHeadin(char):
    if(char == '<'):
        return 1
    if(char == '>'):
        return 3
    if(char == '^'):
        return 2
    if(char == 'v'):
        return 0

class Cart:
    def __init__(self, char, x, y):
        self.x = x
        self.y = y
        self.heading = parseHeadin(char)
        self.nextturn = -1
        self.steps = []
        self.alive = True
    def move(self, map):
        self.steps.append({ 'x' : self.x, 'y' : self.y, 'h' : self.heading})
        if self.heading == 1:
            self.y -= 1
        elif self.heading == 2:
            self.x -= 1
        elif self.heading == 3:
            self.y += 1
        elif self.heading == 0:
            self.x += 1
        self.newDirection(map)
    def newDirection(self, map):
        if (map[self.x][self.y] == '\\'):
            if (self.heading == 1):
                self.heading = 2
            elif (self.heading == 2):
                self.heading = 1
            elif (self.heading == 3):
                self.heading = 0
            elif (self.heading == 0):
                self.heading = 3
        elif (map[self.x][self.y] == '/'):
            if (self.heading == 1):
                self.heading = 0
            elif (self.heading == 2):
                self.heading = 3
            elif (self.heading == 3):
                self.heading = 2
            elif (self.heading == 0):
                self.heading = 1
        elif (map[self.x][self.y] == '+'):
            self.heading = (self.heading + self.nextturn) % 4
            self.nextturn += 1
            if (self.nextturn > 1):
                self.nextturn -= 3
    def hasAnyCollisions(self, carts):
        for cart in carts:            
            if (cart.alive) & (self.collides(cart)):
                cart.alive = False
                self.alive = False
                return True
        return False
    def collides(self, cart):
        return (self.x == cart.x) & (self.y == cart.y) & (self != cart)
    def char(self):
        if self.heading == 1:
            return '<'
        elif self.heading == 2:
            return '^'
        elif self.heading == 3:
            return '>'
        elif self.heading == 0:
            return 'v' 


def cartOrder(cart):
    return cart.x * 1000 + cart.y

def alive(carts):
    al = []
    for cart in carts:
        if cart.alive:
            al.append(cart)
    return al

def removeCarts(line):
    return line.rstrip().replace('>', '-').replace('<', '-').replace('^', '|').replace('v', '|')

def isCart(char):
    return (char == '>') | (char == '<') | (char == 'v') | (char == '^')

def getCarts(line, x):
    carts = []
    line = line.rstrip()
    for y in range(len(line)):
        if(isCart(line[y])):
            carts.append(Cart(line[y], x, y))    
    return carts

def printMap(map, carts):
    m2 = []
    m2.extend(map)
    for cart in carts:
        print(cart.x,cart.y,cart.heading)
        m2[cart.x] = m2[cart.x][0:cart.y] + cart.char() + m2[cart.x][cart.y+1:len(m2[cart.x])]
    for line in m2:
        print(line)
    print('')
    print('')

map = []
carts = []
x = 0
for line in open('rails.txt', 'r').readlines():
    map.append(removeCarts(line))
    carts.extend(getCarts(line, x))
    x += 1

collide = True
ticks = 0
#printMap(map, carts)
while(collide):
    carts.sort(key=cartOrder)
    for cart in carts:
        if not cart.alive:
            continue
        cart.move(map)
        z = cart.hasAnyCollisions(carts)
    ticks += 1
    al = alive(carts)
    if len(al) == 1:
        collide = False        


last = al[0]
print(last.y, last.x)