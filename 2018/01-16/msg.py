import math

class Point:
    def __init__(self, line):
        self.x = int(line.split('<')[1].split(',')[0])
        self.y = int(line.split('>')[0].split(',')[1])
        self.vx = int(line.split('<')[2].split(',')[0])
        self.vy = int(line.split('>')[1].split(',')[1])
    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ">>" + str(self.vx) + ":" + str(self.vy)
    def __repr__(self):
        return str(self.x) + ":" + str(self.y) + ">>" + str(self.vx) + ":" + str(self.vy)
    def move(self):
        self.x += self.vx
        self.y += self.vy


def computeDistance(pts):
    sumx = 0
    sumy = 0
    for pt in pts:
        sumx += pt.x
        sumy += pt.y
    avgx = sumx / len(pts)
    avgy = sumy / len(pts)
    dist = 0
    for pt in pts:
        dist += math.sqrt(abs(pt.x - avgx) * abs(pt.x - avgx) + abs(pt.y - avgy) * abs(pt.y - avgy))
    return dist  

def output(pts, name):
    minx = 100000
    maxx = -100000
    miny = 100000
    maxy = -100000
    for pt in pts:
        if(pt.x > maxx): maxx = pt.x
        if(pt.x < minx): minx = pt.x
        if(pt.y > maxy): maxy = pt.y
        if(pt.y < miny): miny = pt.y
    mat = [['.' for x in range(minx, maxx + 1)] for y in range(miny, maxy + 1)]
    for pt in pts:
        mat[pt.y - miny][pt.x - minx] = '#'
    with open(name, 'a') as the_file:
        for line in mat:
            for char in line:
                the_file.write(char)
            the_file.write('\n')

pts = []
for line in open('msg.txt', 'r').readlines():
    pts.append(Point(line))

for i in range(10450):
    for pt in pts:
        pt.move()

for i in range(20):
    output(pts, str(i))
    for pt in pts:
        pt.move()

    

#for i in range(11000):
#    if((i > 10450) & (i < 10470) & (i % 1 == 0)):
#        print(str(i) + ": " + str(computeDistance(pts)))
#    for pt in pts:
#        pt.move()
    
    

