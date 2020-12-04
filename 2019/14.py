import math
import copy

# This function computes GCD 
def compute_gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

# This function computes LCM
def compute_lcm(x, y):
   lcm = (x*y)//compute_gcd(x,y)
   return lcm

def printDict(dict):
    s = ''
    first = True
    for inp in dict.keys():        
        if first:
            first = False
        else:
            s += ', '
        s += str(dict[inp]) + ' ' + inp
    return s

def multiplyDict(dict, factor):
    for k in dict.keys():
        dict[k] = dict[k] * factor

class Reaction:
    def __init__(self, line):
        parts = line.rstrip().split('=>')
        self.output = { parts[1].split(' ')[2] : int(parts[1].split(' ')[1]) }
        self.input = {}
        for inp in parts[0].split(', '):
            self.input[inp.split(' ')[1]] = int(inp.split(' ')[0])
    def producesFuel(self):
        return 'FUEL' in self.output
    def getOre(self):
        if (len(self.input) == 1) & ('ORE' in self.input):
            return self.input['ORE']
        return 9999999999999999 
    def getOutput(self):
        if len(self.output) > 1:
            print('FUCK! FUCK! FUCK! ABORT!')
            return None
        return next(iter(self.output))
    def multiply(self, modifier):
        multiplyDict(self.input, modifier)
        multiplyDict(self.output, modifier)
    def apply(self, reaction):
        # see if reactions produces ANYTHING we use as input
        o = reaction.getOutput()
        oc = reaction.output[o]
        if o in self.input:
            nc = self.input[o]
            of = math.ceil(nc/oc)
            del self.input[o]
            for ni in reaction.input.keys():
                if ni not in self.input:
                     self.input[ni] = 0
                self.input[ni] = self.input[ni] + (reaction.input[ni] * of)
    def __str__(self):
        return printDict(self.input) + ' => ' + printDict(self.output)
    def __repr__(self):
        return str(self)

def runProg(modifier):
    reacts = []
    for line in open('14.txt', 'r').readlines():
        r = Reaction(line)
        if r.producesFuel():
            r.multiply(modifier)
        reacts.append(r)    
    
    # order reacts by product
    rorder = [] + reacts
    porder = []
    while len(rorder) > 0:
        # find what is not CONSUMED by any other
        found = None
        for r in rorder:
            consumed = False
            for c in rorder:
                if r.getOutput() in c.input:
                    consumed = True
                    break
            if not consumed:
                found = r
                break
        if found is not None:
            porder.append(found)
            rorder.remove(found)
        else:
            print('SHOULD not HAPPEN')
            exit(1)
    
    for i in porder:
        for r in reacts:
            r.apply(i)    
    
    # process in order of product
    minr = 999999999999999
    r = None
    for f in reacts:    
        if f.producesFuel() & (f.getOre() < minr):
            minr = f.getOre()
            r = f
    
    print('#RESULT')
    print(r)
    print(minr < 1000000000000)
    return r


runProg(2876993)                       