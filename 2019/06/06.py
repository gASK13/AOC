class Orbit:
    def __init__(self, line):
        parts = line.strip().split(')')
        self.orbiter = parts[1]
        self.direct = parts[0]
        self.indirect = [parts[0]]

    def __str__(self):
        return '{}){} -> {}){}'.format(self.direct, self.orbiter, ','.join(self.indirect), self.orbiter)

    def __repr__(self):
        return self.__str__()


orbits = []
orbitMap = {}
you = None
san = None
orbitReverseMap = set()
for line in open('06.txt', 'r').readlines():
    orb = Orbit(line)
    orbits.append(orb)
    if orb.direct not in orbitMap:
        orbitMap[orb.direct] = []
    orbitMap[orb.direct].append(orb)
    orbitReverseMap.add(orb.orbiter)
    if orb.orbiter == 'SAN':
        san = orb
    if orb.orbiter == 'YOU':
        you = orb

print(orbitMap)
print(orbitReverseMap)

# ITERATE
to_process = [] + orbits
while len(to_process) > 0:
    processing = None
    for orbit in to_process:
        if orbit.direct not in orbitReverseMap:
            processing = orbit
            orbitReverseMap.remove(orbit.orbiter)
            break

    if processing is None:
        raise Exception("OH NOES!")

    to_process.remove(processing)
    if processing.orbiter in orbitMap:
        for orbit in orbitMap[processing.orbiter]:
            orbit.indirect = processing.indirect + orbit.indirect

#PART ONE
sum = 0
for orbit in orbits:
    sum += len(orbit.indirect)

print(sum)

#PART TWO
print(you)
print(san)

for i in range(max(len(you.indirect), len(san.indirect)), 0, -1):
    if you.indirect[0:i] == san.indirect[0:i]:
        print(len(you.indirect) - i)
        print(len(san.indirect) - i)
        print("PART TWO")
        print((len(san.indirect) - i) + (len(you.indirect) - i))
        break