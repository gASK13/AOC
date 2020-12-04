import math

def fuel(amt):
    part = math.floor(amt / 3)-2
    if (part <= 0):
        return 0
    return part + fuel(part)
    

sum = 0
for line in open('1.txt', 'r').readlines():
    sum += fuel(int(line))

print(sum)


                                                