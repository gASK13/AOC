import common
import copy

class Setup:
    def __init__(self):
        self.floors = [[] for i in range(4)]
        self.prefixes = []
        self.elevator = 0
        self.steps = 0

    def clone(self):
        cl = Setup()
        cl.elevator = self.elevator
        cl.steps = self.steps + 1
        cl.prefixes = self.prefixes
        cl.floors = copy.deepcopy(self.floors)
        return cl


    def init_test(self):
        self.floors = [['HM', 'LM'],
                       ['HG'],
                       ['LG'],
                       []]
        self.prefixes = ['H', 'L']

    def init_real_minus(self):
        self.floors = [['OG', 'TG', 'TM', 'PG', 'CG', 'CM'],
                       ['OM', 'PM'],
                       [],
                       []]
        self.prefixes = ['O', 'T', 'P', 'C']

    def init_real_plus(self):
        self.floors = [['RG', 'RM', 'EG', 'EM', 'OG', 'TG', 'TM', 'PG', 'CG', 'CM'],
                       ['OM', 'PM'],
                       [],
                       []]
        self.prefixes = ['O', 'T', 'P', 'C', 'R', 'E']

    def init_real_two(self):
        self.floors = [['RG', 'RM', 'EG', 'EM', 'OG', 'TG', 'TM', 'PG', 'CG', 'CM', 'DG', 'DE'],
                       ['OM', 'PM'],
                       [],
                       []]
        self.prefixes = ['O', 'T', 'P', 'C', 'R', 'E', 'D']

    def init_real(self):
        self.floors = [['OG', 'TG', 'TM', 'PG', 'RG', 'RM', 'CG', 'CM'],
                       ['OM', 'PM'],
                       [],
                       []]
        self.prefixes = ['O', 'T', 'P', 'R', 'C']

    def next_steps(self):
        moves = []
        for item in self.floors[self.elevator]:
            for i in [-1, +1]:
                if 0 <= self.elevator + i < 4:
                    cl = self.clone()
                    cl.floors[self.elevator].remove(item)
                    cl.floors[self.elevator + i].append(item)
                    cl.elevator += i
                    moves.append(cl)

        if len(self.floors[self.elevator]) >= 2:
            for i1 in range(len(self.floors[self.elevator])):
                for i2 in range(i1 + 1, len(self.floors[self.elevator])):
                    for i in [-1, +1]:
                        if 0 <= self.elevator + i < 4:
                            cl = self.clone()
                            cl.floors[self.elevator].remove(self.floors[self.elevator][i1])
                            cl.floors[self.elevator + i].append(self.floors[self.elevator][i1])
                            cl.floors[self.elevator].remove(self.floors[self.elevator][i2])
                            cl.floors[self.elevator + i].append(self.floors[self.elevator][i2])
                            cl.elevator += i
                            moves.append(cl)
        return moves

    def hash(self):
        for floor in self.floors:
            floor.sort()
        return f"{self.elevator}>>{'$'.join([common.utils.hash_list(floor, '-') for floor in self.floors])}"

    def is_valid(self):
        for floor in self.floors:
            for prefix in self.prefixes:
                if prefix + 'M' in floor and prefix + 'G' not in floor:
                    if len([1 for f in floor if f[1] == 'G' and f[0] != prefix]) > 0:
                        return False
        return True

    def is_win(self):
        return all([len(f) == 0 for f in self.floors[:3]])


# 4 floors
# each step, you can move 1 or 2 items to another floow (!)

# if config was seen - stop
# if M is with diff RTG and not matching RTG = wrong!

# step count + setup

def solve(setup):
    seen = set()
    buffer = [setup]
    i = 0
    while len(buffer) > 0:
        i += 1
        if i % 1000 == 0:
            print(f'{len(buffer)} ({buffer[0].steps})')
        s = buffer.pop(0)
        if s.is_win():
            return s
        for ns in s.next_steps():
            if ns.hash() not in seen and ns.is_valid():
                seen.add(ns.hash())
                buffer.append(ns)
    return None

s = Setup()
s.init_test()
assert solve(s).steps == 11

s = Setup()
s.init_real_minus()
print(solve(s).steps)

s = Setup()
s.init_real()
print(solve(s).steps)

# ok, the asnwer is 12 more steps per pair, so .... 47 + 12 + 12