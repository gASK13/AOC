import re
import operator

class Unit:
    def __init__(self, line, is_immune):
        params = re.fullmatch('([0-9]*) units each with ([0-9]*) hit points ([\(\)a-z, ;]*|)with an attack that does ([0-9]*) ([a-z]*) damage at initiative ([0-9]*)',line).groups()
        self.units = int(params[0])
        self.hp = int(params[1])
        self.damage = int(params[3])
        self.damageType = params[4]
        self.initiative = int(params[5])
        self.weak = []
        self.immune = []
        self.is_immune = is_immune
        self.target = None
        if len(params[2]) > 0:
            weak = re.match('.*weak to ([a-z ,]*)[;\)]', params[2])
            immune = re.match('.*immune to ([a-z ,]*)[;\)]', params[2])
            if weak is not None:
                self.weak = weak.groups()[0].split(', ')
            if immune is not None:
                self.immune = immune.groups()[0].split(', ')

    def formatTypes(self):
        return 'W: {}, I: {}'.format(', '.join(self.weak), ', '.join(self.immune))

    def power(self):
        return self.units * self.damage

    def targetSort(self):
        return self.power() + (self.initiative / 100)

    def take_damage(self, unit):
        dmg = self.calculate_damage(unit)
        dmg = min(dmg, self.units * self.hp)
        self.units -= (dmg // self.hp)
        return dmg

    def calculate_damage(self, unit):
        if unit.damageType in self.immune:
            return 0
        if unit.damageType in self.weak:
            return unit.damage * unit.units * 2
        return unit.damage * unit.units

    def damageSort(self, unit):
        return self.calculate_damage(unit) + (self.targetSort() / 1000000)

    def __repr__(self):
        return '{}: {}@{}HP'.format('IMMUNE' if self.is_immune else 'INFECT', self.units, self.hp)

    def __str__(self):
        return self.__repr__()

    def full_str(self):
        return '{} units, {} HP, {} initiative, {} {} damage ({} power) {}'.format(self.units, self.hp, self.initiative, self.damage, self.damageType, self.power(), self.formatTypes())

def printState(infection, immune):
    print("IMMUNE")
    for unit in immune:
        print(unit.full_str())
    print("INFECT")
    for unit in infection:
        print(unit.full_str())

def turn(infection, immune, debug=False):
    complete = infection + immune
    infection_targets = [] + infection
    immune_targets = [] + immune

    # target selection
    if debug: print('\n\n##### TARGETING #####')
    complete.sort(key = operator.methodcaller('targetSort'), reverse=True)
    for unit in complete:
        trgts = immune_targets
        if unit.is_immune:
            trgts = infection_targets
        trgts.sort(key=operator.methodcaller('damageSort', unit))
        if len(trgts) > 0:
            if trgts[-1].calculate_damage(unit) > 0:
                unit.target = trgts.pop()
                if debug: print('{} -> {}'.format(unit, unit.target if unit.target is not None else 'XXX'))

    # combat!!!
    if debug: print('\n\n##### COMBAT #####')
    complete.sort(key=operator.attrgetter('initiative'))
    while len(complete) > 0:
        unit = complete.pop()
        if unit.target is not None:
            dmg = unit.target.take_damage(unit)
            if debug: print('{} HIT {} FOR {} damage ({} left)'.format(unit, unit.target, dmg, unit.target.units))
            if unit.target.units <= 0:
                if unit.target in complete:
                    complete.remove(unit.target)
                if unit.target.is_immune:
                    immune.remove(unit.target)
                else:
                    infection.remove(unit.target)
            unit.target = None

def compute_status(units):
    ret = 0
    for unit in units:
        ret += unit.units
    return ret

def runSimulation(boost):
    print("##### START #####")
    print(boost)

    infection = []
    immune = []

    is_immune = False
    for line in open('24.txt', 'r').readlines():
        line = line.strip()
        if line == 'Immune System:':
            is_immune = True
        elif line == 'Infection:':
            is_immune = False
        elif len(line) == 0:
            continue
        elif is_immune:
            immune.append(Unit(line, is_immune))
        else:
            infection.append(Unit(line, is_immune))

    for unit in immune:
        unit.damage += boost

    turncount = 0
    last_status = 0
    while (len(infection) > 0) & (len(immune) > 0):
        turn(infection, immune)
        turncount += 1
        if turncount % 100000 == 0:
            print("Turn: {}, Status: {}".format(turncount, compute_status(infection + immune)))
        if last_status == compute_status(infection + immune):
            break
        last_status = compute_status(infection + immune)

    print('\n\n##### END #####')
    print('{} WON @ TURN {}: {}'.format('INFECTION' if len(infection) > 0 else 'IMMUNE', turncount, compute_status(infection + immune)))

    if len(infection) == 0:
        return True
    return False

boost = (0, 1024)
while True:
    if boost[0] == boost[1]:
        print('Minimal boost: {}'.format(boost[0]))
        break
    half = int((boost[0] + boost[1]) / 2)
    if runSimulation(half):
        boost = (boost[0], half)
    else:
        boost = (half + 1, boost[1])

