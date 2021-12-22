import common


class Cube:
    def __init__(self, line=None, axes=None, on=True):
        if line is None:
            self.on = on
            self.__axes = axes
        else:
            self.on = True if line.split(' ')[0] == 'on' else False
            self.__axes = [[int(x) for x in line.split(',')[0].split('=')[1].split('..')],
                           [int(y) for y in line.split(',')[1].split('=')[1].split('..')],
                           [int(z) for z in line.split(',')[2].split('=')[1].split('..')]]

    def __intersects(self, other):
        for i in range(3):
            if self.__axes[i][0] > other.__axes[i][1] or self.__axes[i][1] < other.__axes[i][0]:
                return False
        return True

    def __str__(self):
        return '~'.join(['..'.join([str(n) for n in a]) for a in self.__axes])

    def __repr__(self):
        return self.__str__()

    def volume_limit(self, nr):
        test_cube = Cube(axes=[[-nr, nr], [-nr, nr], [-nr, nr]])
        if not self.__intersects(test_cube):
            return 0
        vol = 1
        for a in self.__axes:
            vol *= min(a[1], nr) - max(a[0], -nr) + 1
        return vol

    def break_by(self, other):
        if self.__intersects(other):
            breaks = self.get_breaks(other)
            broken_cubes = []
            for bx in breaks[0]:
                for by in breaks[1]:
                    for bz in breaks[2]:
                        if any([bx[2], by[2], bz[2]]):
                            broken_cubes.append(Cube(axes=[[bx[0], bx[1]], [by[0], by[1]], [bz[0], bz[1]]]))
            # break by other
            # each axis can be -> whole within (single OFF)
            # before / after / around -> whole within / outside
            return broken_cubes
        return [self]

    def get_breaks(self, other):
        breaks = [[], [], []]
        for i in range(3):
            if other.__axes[i][0] > self.__axes[i][0]:
                # the begining is "plus"
                if other.__axes[i][1] < self.__axes[i][1]:
                    # the ending is "plus" and there is "minus"
                    breaks[i].append([self.__axes[i][0], other.__axes[i][0] - 1, True])
                    breaks[i].append([other.__axes[i][0], other.__axes[i][1], False])
                    breaks[i].append([other.__axes[i][1] + 1, self.__axes[i][1], True])
                else:
                    # the other half is minus
                    breaks[i].append([self.__axes[i][0], other.__axes[i][0] - 1, True])
                    breaks[i].append([other.__axes[i][0], self.__axes[i][1], False])
            else:
                # the begining element is "minus"
                if other.__axes[i][1] < self.__axes[i][1]:
                    # the ending is "plus"
                    breaks[i].append([self.__axes[i][0], other.__axes[i][1], False])
                    breaks[i].append([other.__axes[i][1] + 1, self.__axes[i][1], True])
                else:
                    # the whole part is minus
                    breaks[i].append([self.__axes[i][0], self.__axes[i][1], False])
        return breaks


def calculate_volume(file=None, limit=50):
    cubes_filter = common.Loader.transform_lines(Cube, file)
    on_cubes = []
    for c in cubes_filter:
        # try to intersect with each cube in ON
        new_on_cubes = [c] if c.on else []
        for oc in on_cubes:
            new_on_cubes += oc.break_by(c)
        on_cubes = new_on_cubes
    return sum([v.volume_limit(limit) for v in on_cubes])


# TEST PART ONE
print(calculate_volume('test_simple.txt'))
assert calculate_volume('test_simple.txt') == 39
print(calculate_volume('test.txt'))
assert calculate_volume('test.txt') == 590784

# PART TWO
print(calculate_volume('test_large.txt', limit=1000000))
assert calculate_volume('test_large.txt', limit=1000000) == 2758514936282235

# REAL!!!
print(calculate_volume())
print(f'REAL = {calculate_volume()}')
print(f'REAL PT 2= {calculate_volume(limit=1000000)}')

# REAL IS 545118 (naive)