import common
import re


class Sensor:
    def __init__(self, line):
        (self.x, self.y, self.bx, self.by) = [int(m) for m in re.compile('=([\-0-9]*)').findall(line)]
        self.md = abs(self.x - self.bx) + abs(self.y - self.by)

    def get_x_range(self, y):
        md = self.md - abs(y - self.y)
        return (self.x - md, self.x + md) if self.x + md > self.x - md else None

    def can_detect(self, x, y):
        return abs(x - self.x) + abs(y - self.y) <= self.md


def merge_ranges(ranges, new_range, purge_negatives = False):
    retrngs = []
    if new_range is None:
        return ranges
    else:
        last_i = None
        for interval in sorted(ranges + [new_range]):
            if purge_negatives and interval[1] < 0:
                continue
            if purge_negatives and interval[0] < 0:
                interval = (0, interval[1])
            if last_i is None:
                last_i = interval
            else:
                if last_i[1] + 1 >= interval[0]:
                    if last_i[1] >= interval[1]:
                        # skip, we ate it
                        pass
                    else:
                        last_i = (last_i[0], interval[1])
                else:
                    retrngs.append(last_i)
                    last_i = interval
        if last_i is not None:
            retrngs.append(last_i)
    return retrngs


def get_covered_x(sensors, y):
    xes = []
    for s in sensors:
        xes = merge_ranges(xes, s.get_x_range(y))
    cnt = sum([en - st + 1 for st, en in xes])
    cnt -= len(set([s.bx for s in sensors if s.by == y]))
    return cnt


def find_beacon(sensors, max):
    for y in range(max):
        print(y)
        xes = []
        for s in sensors:
            xes = merge_ranges(xes, s.get_x_range(y), True)
            if len(xes) == 1 and xes[0][0] == 0 and xes[0][0] >= max:
                break #full ine
        if len(xes) > 1:
            return xes[0][1] + 1, y
    return None


def get_frequency(sensors, max):
    x, y = find_beacon(sensors, max)
    return x*4000000 + y

assert merge_ranges([(1,5), (9, 12)], (3, 7)) == [(1, 7), (9, 12)]
assert merge_ranges([(1,5), (9, 12)], (3, 10)) == [(1, 12)]
assert merge_ranges([], None) == []
assert merge_ranges([], (1, 2)) == [(1, 2)]
assert merge_ranges([(1, 2), (5,7)], None) == [(1,2), (5,7)]
assert merge_ranges([(1, 4), (9, 12)], (5, 8)) == [(1, 12)]

assert get_covered_x(common.Loader.transform_lines(Sensor, 'test'), 10) == 26
print(f'Possible beacon count is {get_covered_x(common.Loader.transform_lines(Sensor), 2000000)}')

assert find_beacon(common.Loader.transform_lines(Sensor, 'test'), 20) == (14, 11)
assert get_frequency(common.Loader.transform_lines(Sensor, 'test'), 20) == 56000011
print(f'Final frequency is {get_frequency(common.Loader.transform_lines(Sensor), 4000000)}')