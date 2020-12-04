class Rule:
    def __init__(self, rule, output):
        self.rule = rule
        self.output = output
    def __str__(self):
        return self.rule + " => " + self.output
    def __repr__(self):
        return self.rule + " => " + self.output


def parseState(line):
    return ('.' * 100) + line.rstrip().split(' ')[2] + ('.' * 800)

def parseRule(line):
    l = line.rstrip()
    if (len(l) == 0):
        return None
    else:
        return Rule(l.split(' ')[0], l.split(' ')[2])

frst = True
rules = []
initial = None
for line in open('plant.txt', 'r').readlines():
    if (frst):
        initial = parseState(line)
        frst = False
    else:
        rule = parseRule(line)
        if(rule != None):
            rules.append(rule)

curgen = initial
nextgen = ''

with open('plant.out', 'a') as the_file:
    for i in range(500):
        for j in range(len(curgen)):
            if ((j < 2) | (j > (len(curgen) - 3))):
                nextgen += curgen[j]
            else:
                mask = curgen[j-2:j+3]
                for rule in rules:
                    if (rule.rule == mask):
                        nextgen += rule.output
        curgen = nextgen
        nextgen = ''
        b = the_file.write(curgen)
        b = the_file.write('\n')


tot = 0
cnt = 0
for i in range(len(curgen)):
    if(curgen[i] == '#'):
        tot += (i - 100)
        cnt += 1


