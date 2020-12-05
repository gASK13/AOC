def placewire(x,y,mat,exes):
    if mat[x][y] == '-':
        mat[x][y] = 'X'
        exes.append([x,y])
    else:
        mat[x][y] = '-' 

def printMap(mat):
    for line in mat:
        print(''.join(line))

size = 50000
mat = [['.' for z in range(0,size)] for y in range(0,size)]
mats = [[[0 for z in range(0,size)] for y in range(0,size)],[[0 for z in range(0,size)] for y in range(0,size)]]

wires = []
for line in open('3.txt', 'r').readlines():
    wires.append(line.split(','))
    
#wires = [['R8','U5','L5','D3'],['U7','R6','D4','L4']]
#wires = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],['U62','R66','U55','R34','D71','R55','D58','R83']]
#wires = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]    

exes = [] 
wi = 0
for wire in wires:
    sx = int(size/2)
    sy = int(size/2)
    steps = 0
    mat[sx][sy] = 'o'
    for step in wire:
        if step[0] == 'R':
            for x in range(1,int(step[1:])):
                placewire(sx+x, sy, mat, exes)
                if mats[wi][sx+x][sy] == 0: mats[wi][sx+x][sy] = steps + x 
            sx = sx+int(step[1:])
        elif step[0] == 'L':
            for x in range(1,int(step[1:])):
                placewire(sx-x, sy, mat, exes)
                if mats[wi][sx-x][sy] == 0: mats[wi][sx-x][sy] = steps + x
            sx = sx-int(step[1:])
        elif step[0] == 'D':
            for x in range(1,int(step[1:])):
                placewire(sx, sy+x, mat, exes)
                if mats[wi][sx][sy+x] == 0: mats[wi][sx][sy+x] = steps + x
            sy = sy+int(step[1:])
        elif step[0] == 'U':
            for x in range(1,int(step[1:])):
                placewire(sx, sy-x, mat, exes)
                if mats[wi][sx][sy-x] == 0: mats[wi][sx][sy-x] = steps + x
            sy = sy-int(step[1:])        
        steps += int(step[1:])
        if mats[wi][sx][sy] == 0: mats[wi][sx][sy] = steps
        print(str(wi) + "#" + str(steps))
        mat[sx][sy] = '+'
    wi += 1

min = 9999999
minx = 0
miny = 0
sx = int(size/2)
sy = int(size/2)
print(len(exes))
for ex in exes:
    if (mats[0][ex[0]][ex[1]] == 0) | (mats[1][ex[0]][ex[1]] == 0): continue
    dist = mats[0][ex[0]][ex[1]] + mats[1][ex[0]][ex[1]]
    if (dist < min):
        min = dist
        minx = ex[0]
        miny = ex[1]
            

#printMap(mat)
print(min)
print(minx)
print(miny)