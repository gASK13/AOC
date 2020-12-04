class Linea:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
    def __str__(self):
        return self.src + "->" + self.dst
    def __repr__(self):
        return self.src + "->" + self.dst
        
def parseLine(line):
    return Linea(line[5], line[36])

def workStep(wrkrs):
    done = []
    total = 0
    while(len(done) == 0):
        for wrk in wrkrs:
            wrkrs[wrk] -= 1
            if (wrkrs[wrk] == 0): done.append(wrk)
        total += 1
    return { 'done': done, 'time' : total }


srcs = {}
dsts = {}
wip = {}
wrkrs = {}
for line in open('gr.txt', 'r').readlines():
    ln = parseLine(line)
    if ln.src not in srcs:
        srcs[ln.src] = [] 
    srcs[ln.src].append(ln)
    if ln.dst not in dsts:
        dsts[ln.dst] = []
    dsts[ln.dst].append(ln)

output = ''
total = 0
while (len(srcs) > 0):
    next = 'ZZZ'
    for src in srcs:
        if (src not in dsts):
            if ((next > src)):
                next = src
    
    if (next == 'ZZZ'):
        done = workStep(wrkrs)
        total += done['time']
        for dn in done['done']:
            b = wrkrs.pop(dn)
            nextlines = wip.pop(dn)
            for nl in nextlines:
                dsts[nl.dst].remove(nl)
                if (len(dsts[nl.dst]) == 0): a = dsts.pop(nl.dst)
                if (nl.dst not in srcs): srcs[nl.dst] = []
        continue
    
    wrkrs[next] = ord(next) - 4     
    wip[next] = srcs.pop(next)
    
    if (len(wrkrs) == 5):
        done = workStep(wrkrs)
        total += done['time']
        for dn in done['done']:
            b = wrkrs.pop(dn)
            nextlines = wip.pop(dn)
            for nl in nextlines:
                dsts[nl.dst].remove(nl)
                if (len(dsts[nl.dst]) == 0): a = dsts.pop(nl.dst)
                if (nl.dst not in srcs): srcs[nl.dst] = []
                
                








    
    
        


