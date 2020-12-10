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
r = [0,0,0,0,0,0]
#r = [2047, 4, 10551300, 10551300, 10551306, 1]
first = True
for line in open('code_ip.txt', 'r').readlines():
    if first:
        first = False
        ip = int(line.split(' ')[1])
    else:
        program.append(Code(line))

run = True
with open('p0', 'a') as the_file:
    o = the_file.write(str(r) + '\n')
    while run:
        p = program[r[ip]]
        r[p.c] = globals()[p.instruction](r, p.a, p.b)
        r[ip] += 1
        if (r[ip] >= len(program)):
            run = False
        o = the_file.write(str(r) + '\n')

    

r0 = 0
r4 = 10551306
#r4 = 906 
r5 = 1
while r5 <= r4:
    r2 = 1
    while r2 <= r4:
        r3 = r5 * r2
        if r3 == r4:
            r0 += r5
        r2 += 1
    r5 += 1

r0 = 0
r4 = 10551306
for r5 in range(1,r4+1):
    if (r4 / r5) == int(r4 / r5):
        r0 += r5

r0