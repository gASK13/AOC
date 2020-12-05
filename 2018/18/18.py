import hashlib

def computeHash(map):
    return hashlib.md5('X'.join(map).encode('utf-8')).hexdigest()

def printMap(mat):
    for line in mat:
        print(''.join(line))

def countAround(map, x, y, char):
    cnt = 0
    for ex in range(x-1, x+2):
        for ey in range(y-1, y+2):
            if (ey >= 0) & (ex >= 0) & (ey < len(map)) & (ex < len(map[0])):
                if (map[ey][ex] == char) & ((ex != x) | (ey != y)):
                    cnt += 1
    return cnt

def count(map, char):
    cnt = 0
    for line in map:
        for ch in line:
            if ch == char:
                cnt += 1
    return cnt

def processMap(map):
    newMap = []
    for (row, line) in enumerate(map):
        newLine = ''
        for (col, char) in enumerate(line):
            if char == '.':
                if countAround(map, col, row, '|') >= 3:
                    newLine += '|'
                else:
                    newLine += '.'
            if char == '#':
                if (countAround(map, col, row, '#') >= 1) & (countAround(map, col, row, '|') >= 1):
                    newLine += '#'
                else:
                    newLine += '.'
            if char == '|':
                if countAround(map, col, row, '#') >= 3:
                    newLine += '#'
                else:
                    newLine += '|'
        newMap.append(newLine)
    return newMap

map = []
steps = {}
for line in open('18.txt', 'r').readlines():
    map.append(line.strip())
#printMap(map)
steps[computeHash(map)] = { 'map' : map, 'step' : 0 }

i = 1
skipped = False
while i < 1000000001:
    print(str(i) + " minute:")
    map = processMap(map)
    #printMap(map)
    hsh = computeHash(map)
    if (not skipped) & (hsh in steps):
        curr = i
        last = steps[hsh]['step']
        step = curr - last
        while i + step < 1000000000:
            i += step
        skipped = True
    steps[hsh] = { 'map' : map, 'step' : i }
    i += 1


lumber = count(map, '#')
wood = count(map, '|')
print("Lumberyards: " + str(lumber))
print("Woods: " + str(wood))
print(wood * lumber)

