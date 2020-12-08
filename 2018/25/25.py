import re
import numpy as np


class Point:
    def __init__(self, line):
        coords = re.findall('(-?[0-9]+)', line)
        self.coords = np.array([int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])])

    def distance(self, other):
        return abs(self.coords - other.coords).sum()


def are_same(c1, c2):
    for s1 in c1:
        for s2 in c2:
            if s1.distance(s2) <= 3:
                return True
    return False

# read data
constellations = []
for line in open('25.txt', 'r').readlines():
    constellations.append([Point(line.strip())])

# compute constellations
new_constellations = []
changed = False
while True:
    con = constellations.pop()
    cons = []
    for con2 in constellations:
        if are_same(con, con2):
            cons.append(con2)
            con = con + con2
            changed = True
    for con2 in cons:
        constellations.remove(con2)
    new_constellations.append(con)
    if len(constellations) == 0:
        print('Running: {}'.format(len(new_constellations)))
        constellations = new_constellations
        new_constellations = []
        if not changed:
            break
        else:
            changed = False

print(len(constellations))




