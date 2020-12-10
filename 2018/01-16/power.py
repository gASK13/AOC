def computePowerLevel(x, y, seed):
    rackid = x + 10
    plv = rackid * y
    plv += seed
    plv *= rackid
    hd = int((plv - (plv % 100)) / 100) % 10
    return hd - 5 

def computePowerTotal(x, y, seed, size):
    tot = 0
    for i in range(x, x+size):
        for j in range(y, y+size):
            tot += computePowerLevel(i, j, seed)
    return tot

seed = 8444

max = 0
maxc = None
mat = [[[0 for z in range(0,300)] for y in range(0,300)] for x in range(0,300)]
for x in range(0, 300):
    for y in range(0, 300):
        tot = computePowerLevel(x+1,y+1, seed)
        mat[0][x][y] = tot 
        if (tot > max):
            maxc = { 'x' : x+1, 'y' : y+1, 'size' : 1 }
 
for size in range(1,300):
    TODO - odzadu a sumuj
    for x in range(1, 300 - size + 2):
        for y in range(1, 300 - size + 2):
            tot = computePowerTotal(x, y, seed, size)
            if (tot > max):
                max = tot
                maxc = { 'x' : x, 'y' : y, 'size' : size }

print(max, maxc)