import math

cnt = 0
for x in range(236491,713787):
    dbl = False
    dcr = True
    digs = [0 for i in range(0,10)]
    prev = -1
    order = 1000000
    while order > 1:
        now = math.floor((x % order) / (order / 10))
        if (now < prev): dcr = False
        digs[now] += 1
        order = order / 10
        prev = now
    for i in range(0,10):
        if digs[i] == 2: dbl = True
    if dbl & dcr: 
        cnt += 1

print(cnt)
    
     
                                                