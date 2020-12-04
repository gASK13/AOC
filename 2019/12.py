import math

# This function computes GCD 
def compute_gcd(x, y):
   while(y):
       x, y = y, x % y
   return x
# This function computes LCM
def compute_lcm(x, y):
   lcm = (x*y)//compute_gcd(x,y)
   return lcm
   
class Moon:
    def __init__(self, line):
        parts = line.split('<')[1].split('>')[0].split(',')
        self.pos = {}
        self.vel = {}
        self.pos['x'] = int(parts[0].split('=')[1])
        self.pos['y'] = int(parts[1].split('=')[1])
        self.pos['z'] = int(parts[2].split('=')[1])
        self.vel['x'] = 0
        self.vel['y'] = 0
        self.vel['z'] = 0    
    def __str__(self):    
        return 'pos=<x=' + str(self.pos['x']) + ', y=' + str(self.pos['y']) + ' ,z=' + str(self.pos['z']) + '>, vel=<x=' + str(self.vel['x']) + ', y=' + str(self.vel['y']) + ' ,z=' + str(self.vel['z']) + '>'
    def __repr__(self):
        return 'pos=<x=' + str(self.pos['x']) + ', y=' + str(self.pos['y']) + ' ,z=' + str(self.pos['z']) + '>, vel=<x=' + str(self.vel['x']) + ', y=' + str(self.vel['y']) + ' ,z=' + str(self.vel['z']) + '>'
    def move(self):
        self.move('x')
        self.move('y')
        self.move('z')
    def move(self, axis):
        self.pos[axis] += self.vel[axis]
    def energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.vx) + abs(self.vy) + abs(self.vz))
    def gravity(self, other):
        self.gravity(other, 'x')
        self.gravity(other, 'y')
        self.gravity(other, 'z')
    def gravity(self, other, axis):
        if self.pos[axis] < other.pos[axis]:
            self.vel[axis] += 1
            other.vel[axis] -= 1
        elif self.pos[axis] > other.pos[axis]:
            self.vel[axis] -= 1
            other.vel[axis] += 1    
    def hash(self):
        return self.hash('x') + self.hash('y') + self.hash('z')
    def hash(self, axis):
        return str(self.pos[axis]) + '#' + str(self.vel[axis]) + "@"

def hash(moons, axis):
    s = ''
    for moon in moons:
        s += moon.hash(axis);
    return s        

def move(moons, axis):
    for a in range(0,len(moons)):
        for b in range(a+1,len(moons)):
            moons[a].gravity(moons[b], axis)
    for moon in moons:
        moon.move(axis)

def moveAxis(moons, axis):
    print(axis)
    steps = { hash(moons, axis) : 0 }
    i = 0
    while True:
        move(moons, axis)
        hsh = hash(moons, axis)
        i += 1
        if (hsh in steps):
            break        
        steps[hsh] = i
        if i % 100000 == 0:
            print(i)                

    return i    
    
moons = []
for line in open('12.txt', 'r').readlines():
    moons.append(Moon(line))

xa = moveAxis(moons, 'x')
ya = moveAxis(moons, 'y')
za = moveAxis(moons, 'z')

print(xa)
print(ya)
print(za)
print(compute_lcm(xa, compute_lcm(ya, za)))                                                