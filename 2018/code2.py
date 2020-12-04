class Code:
    def __init__(self, line):
        split = line.rstrip().split(' ')
        self.instruction = split[0]
        self.a = int(split[1])
        self.b = int(split[2])
        self.c = int(split[3])
    def __str__(self):
        return self.instruction + " " + str(self.a) + "+" + str(self.b) + "=" + str(self.c)
    def __repr__(self):
        return self.instruction + " " + str(self.a) + "+" + str(self.b) + "=" + str(self.c)

def addr(reg, a, b):
    return reg[a] + reg[b]

def addi(reg, a, b):
    return reg[a] + b

def mulr(reg, a, b):
    return reg[a] * reg[b]

def muli(reg, a, b):
    return reg[a] * b

def banr(reg, a, b):
    return reg[a] & reg[b]

def bani(reg, a, b):
    return reg[a] & b

def borr(reg, a, b):
    return reg[a] | reg[b]

def bori(reg, a, b):
    return reg[a] | b    

def setr(reg, a, b):
    return reg[a]

def seti(reg, a, b):
    return a

def gtir(reg, a, b):
    if a > reg[b]:
        return 1
    return 0

def gtri(reg, a, b):
    if reg[a] > b:
        return 1
    return 0

def gtrr(reg, a, b):
    if reg[a] > reg[b]:
        return 1
    return 0

def eqir(reg, a, b):
    if a == reg[b]:
        return 1
    return 0

def eqri(reg, a, b):
    if reg[a] == b:
        return 1
    return 0

def eqrr(reg, a, b):
    if reg[a] == reg[b]:
        return 1
    return 0

ip = 0
program = []

first = True
for line in open('code21.txt', 'r').readlines():
    if first:
        first = False
        ip = int(line.split(' ')[1])
    else:
        program.append(Code(line))

run = True
iter = 0
r = [0,0,0,0,0,0]     

    while run:
        if r[ip] == 28:
            o = the_file.write(str(r) + '\n')
            o = the_file.flush()
        p = program[r[ip]]
        r[p.c] = globals()[p.instruction](r, p.a, p.b)
        r[ip] += 1
        iter += 1
        if (r[ip] >= len(program)):
            run = False

print(iter)
    
    
[0, 155, 28, 13528820, 1, 1]    
    
    
import math
seen = []
def ptr5(r, the_file):
    while True:
        r[1] = r[3] | 65536
        r[3] = 4921097
        while True:
            r[3] = r[3] + (r[1] & 255)
            r[3] = r[3] & 16777215
            r[3] = r[3] * 65899
            r[3] = r[3] & 16777215
            if r[1] < 256:
                if r[3] in seen:
                    print ("WOOT! REPEATING!")
                    return True
                seen.append(r[3])
                o = the_file.write(str(r) + '\n')
                o = the_file.flush()
                if r[3] == r[0]:
                    return True
                break
            r[4] = 0
            r[1] = math.floor(r[1]/256)

r = [0,0,0,0,0,0]      
with open('p0', 'w') as the_file:  
    ptr5(r, the_file)




	    