class Code:
    def __init__(self, lines):
        self.before = parseLine(lines[0])
        self.code = parseLine(lines[1])
        self.after = parseLine(lines[2])
    def __str__(self):
        return str(self.before) + "/" + str(self.code) + "/" + str(self.after)
    def __repr__(self):
        return str(self.before) + "/" + str(self.code) + "/" + str(self.after)

def parseLine(line):
    if '[' in line:
        line = line.split('[')[1].split(']')[0].replace(',', '')
    arr = []
    for ch in line.split(' '):
        arr.append(int(ch))
    return arr

def allEmpty(lines):
    for line in lines:
        if len(line) > 0: return False
    return True

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

funcs = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
pc = [[True for x in range(16)] for y in range(16)]
sorted_funcs = [None for x in range(16)]
triad = []
codes = []
emptycnt = 0
program = []
r = [0,0,0,0]
for line in open('code.txt', 'r').readlines():
    if emptycnt > 2:
        if len(line.rstrip()) > 0:
            program.append(parseLine(line))
        continue
    if len(line.rstrip()) > 0: 
        triad.append(line.rstrip())
        emptycnt = 0
    else:
        emptycnt += 1
    if len(triad) == 3:
        codes.append(Code(triad))
        triad = []

for code in codes:
    for fn in funcs:
        if (fn(code.before, code.code[1], code.code[2]) == code.after[code.code[3]]):
            #rght += 1
            print('WTF')
        else:
            pc[funcs.index(fn)][code.code[0]] = False

while len(list(filter(lambda fn : len(list(filter(lambda x : x == True, fn))) > 1, pc))) > 0:
    for item in list(filter(lambda fn : len(list(filter(lambda x : x == True, fn))) == 1, pc)):
        fnidx = pc.index(item)
        idx = item.index(True)
        for fn in pc:
            if fn != item:
                fn[idx] = False

for fn in pc:
    idx = fn.index(True)
    sorted_funcs[idx] = funcs[pc.index(fn)]


for p in program:
    r[p[3]] = sorted_funcs[p[0]](r, p[1], p[2])

print(r)

    

