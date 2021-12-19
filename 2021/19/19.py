import common


class Scanner:
    def __init__(self, lines):
        self.id = lines.pop(0).split(' ')[2]
        self.__beacons = []
        self.__coords = (0, 0, 0)
        while len(lines) > 0:
            line = lines.pop(0)
            self.__beacons.append([int(i) for i in line.split(',')])

    def __str__(self):
        return f'{self.id} >>> {self.__beacons}'

    def __repr__(self):
        return f'{self.id} >>> {self.__beacons}'

    def __rotations(self):
        results = []
        # add 3 facings
        temps = [[[x, y, z] for x, y, z in self.__beacons]]
        temps += [[[y, -x, z] for x, y, z in self.__beacons]]
        temps += [[[z, y, -x] for x, y, z in self.__beacons]]
        # flip them (facing -x,-y and -z)
        temps += [[[-x, y, -z] for x, y, z in t] for t in temps]
        # now rotate them 4 directions
        for i in range(4):
            results += temps
            temps = [[[x, z, -y] for x, y, z in t] for t in temps]
        return results

    def beacon_set(self):
        return set([(x, y, z) for x, y, z in self.__beacons])

    def manhattan_distance(self, other):
        return abs(self.__coords[0] - other.__coords[0]) + abs(self.__coords[1] - other.__coords[1]) + abs(self.__coords[2] - other.__coords[2])

    def match_to_beacon(self, other):
        # for each rotation
        for rotation in self.__rotations():
            # for each pair of beacons
            for bs in rotation:
                for bo in other.__beacons:
                    dx, dy, dz = bo[0] - bs[0], bo[1] - bs[1], bo[2] - bs[2]
                    # try to "shift" to match the other
                    moved = [[x + dx, y + dy, z + dz] for x, y, z in rotation]
                    matches = 0
                    for bm in moved:
                        if bm in other.__beacons:
                            matches += 1
                    # overlaps at least 12? return
                    if matches >= 12:
                        self.__beacons = moved
                        self.__coords = (dx, dy, dz)
                        return True
        return False


def find_matching_scanner(matched, unmatched):
    matches = []
    for s in unmatched:
        if s.match_to_beacon(matched):
            matches.append(s)
    return matches


def reduce_scanners(_scanners):
    scnrs = [s for s in _scanners]  # copy
    match = [scnrs.pop(0)]
    beacons = set()
    while len(match) > 0:
        print(f'{len(match)} / {len(scnrs)}')
        last_match = match.pop(0)
        beacons = set.union(beacons, last_match.beacon_set())
        matches = find_matching_scanner(last_match, scnrs)
        match += matches
        for m in matches:
            scnrs.remove(m)
    if len(scnrs) > 0:
        raise RuntimeError("OOPS! Not mached?")
    return beacons


def largest_distance(_scanners):
    return max([s.manhattan_distance(s2) for s in _scanners for s2 in _scanners])


scanners = common.Loader.transform_lines_complex(Scanner, filename='test.txt')
bcns = reduce_scanners(scanners)
print(f'Test = {len(bcns)}, expected = 79')
print(f'Test = {largest_distance(scanners)}, expected = 3621')

scanners = common.Loader.transform_lines_complex(Scanner)
bcns = reduce_scanners(scanners)
print(f'Real = {len(bcns)}, distance {largest_distance(scanners)}')
