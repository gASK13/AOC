def parsePt(line):
    return { 'x': int(line.split(',')[0]), 'y' : int(line.split(',')[1]) , 'cnt' : 0, 'touches': False }

def computeDistance(i,j,pt):
    return abs(i-pt['x']) + abs(j-pt['y'])    

pts = []
x = 1000
y = 1000
ex = 0
ey = 0
for line in open('input3.txt', 'r').readlines():
    pt = parsePt(line)
    if (pt['x'] < x): x = pt['x']
    if (pt['y'] < y): y = pt['y']
    if (pt['x'] > ex): ex = pt['x']
    if (pt['y'] > ey): ey = pt['y'] 
    pts.append(pt)

ttarea = 0
for i in range(x,ex+1):
    for j in range(y,ey+1):
        maxpt = None
        maxdist = 10000
        maxone = True
        totdist = 0
        for pt in pts:
            dist = computeDistance(i,j,pt)
            totdist += dist
            if (dist == maxdist):
                maxone = False
                maxpt = None
            if (dist < maxdist):
                maxdist = dist
                maxpt = pt
                maxone = True
        if((maxone == True) & (maxpt != None)):
            maxpt['cnt'] += 1
            if((i == x) | (j == y) | (i == ex) | (j == ey)):
                maxpt['touches'] = True
        if(totdist < 10000):
            ttarea += 1

maxpt = None
maxarea = 0
for pt in pts:
    if(pt['touches'] == False):
        if(pt['cnt'] > maxarea):
            maxarea = pt['cnt']
            maxpt = pt

print(maxpt)
print(ttarea)