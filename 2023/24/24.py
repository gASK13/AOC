import common
from colorama import Fore, Back, Style
import sympy as sp
from sympy import linsolve, symbols, solve, solveset


class Hailstone:
    def __init__(self, line=None, x=0, y=0, z=0, vx=0, vy=0, vz=0):
        if line is not None:
            coords, diffs = line.split(' @ ')
            self.coords = [int(x) for x in coords.split(', ')]
            self.vectors = [int(x) for x in diffs.split(', ')]
        else:
            self.coords = [x, y, z]
            self.vectors = [vx, vy, vz]

    def find_intersect_xy(self, other):
        # I need to find intersect of the two lines irrespective time
        xdiff = (self.vectors[0], other.vectors[0])
        ydiff = (self.vectors[1], other.vectors[1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = (det((self.coords[0] + self.vectors[0], self.coords[1] + self.vectors[1]), (self.coords[0], self.coords[1])), det((other.coords[0] + other.vectors[0], other.coords[1] + other.vectors[1]), (other.coords[0], other.coords[1])))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        # now check if this is "forward" in time, so if t >= 0 for both
        t1 = (x - self.coords[0]) / self.vectors[0]
        t2 = (x - other.coords[0]) / other.vectors[0]
        if t1 < 0 or t2 < 0:
            return None
        return x, y

    def find_collision_axis(self, other, axis):
        if self.vectors[axis] == other.vectors[axis]:
            if self.coords[axis] == other.vectors[axis]:
                return 0 # this means "any"
            else:
                return None
        time = (self.coords[axis] - other.coords[axis]) / (other.vectors[axis] - self.vectors[axis])
        if time < 0:
            return None
        return time

    def find_collision_3d(self, other):
        times = [None, None, None]
        for i in range(3):
            times[i] = self.find_collision_axis(other, i)
        if None in times:
            return None
        # either all equal of one is 0
        mt = max(times)
        if all([t in [0, mt] for t in times]):
            return mt
        return None


def find_collision_pairs(hailstones, min, max):
    collisions = []
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            collision = hailstones[i].find_intersect_xy(hailstones[j])
            if collision is not None and min <= collision[0] <= max and min <= collision[1] <= max:
                collisions.append((i, j, collision))
    return collisions



def throw_rock(hailstones):
    # try it with equations!
    # for each pair, the equation is
    # x + dx * t1 - (hx + hx * t1) for each axis
    syms = symbols('rx, ry, rz, rdx, rdy, rdz')
    coords = syms[0:3]
    vectors = syms[3:6]
    syms = list(syms)
    eqs = []
    # THIS IS THE SMART PART - ANY THREE LINES DENOTE THE WHOLE SOLUTION!!!! DUH!!!
    # Could have done this manually (ouch), but instead I used sympy cause I already started
    for i in range(3):
        t = symbols(f't{i}')
        syms.append(t)
        for a in range(3):
            eqs.append(hailstones[i].coords[a] - coords[a] + t * (hailstones[i].vectors[a] - vectors[a]))
    retval = solve(eqs, syms)
    print(retval)
    return retval[0][0], retval[0][1], retval[0][2]


assert len(find_collision_pairs(common.Loader.transform_lines(Hailstone, 'test'), 7, 27)) == 2
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{len(find_collision_pairs(common.Loader.transform_lines(Hailstone), 200000000000000, 400000000000000))}')

assert sum(throw_rock(common.Loader.transform_lines(Hailstone, 'test'))) == 47
print(f'Part 2: {Back.GREEN}{Fore.BLACK}{sum(throw_rock(common.Loader.transform_lines(Hailstone)))}')

