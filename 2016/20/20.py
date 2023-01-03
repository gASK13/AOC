import common


def merge_ranges(ranges, new_range):
    retrngs = []
    if new_range is None:
        return ranges
    else:
        last_i = None
        for interval in sorted(ranges + [new_range]):
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


def find(lines):
    ranges = []
    for line in lines:
        ranges = merge_ranges(ranges, tuple([int(c) for c in line.split('-')]))
    if ranges[0][0] > 0:
        return 0
    return ranges[0][1] + 1


def find_all(lines, max):
    ranges = []
    for line in lines:
        ranges = merge_ranges(ranges, tuple([int(c) for c in line.split('-')]))
    sm = 0
    for i in range(len(ranges) + 1):
        mi = -1 if i == 0 else ranges[i-1][1]
        mx = max + 1 if i >= len(ranges) else ranges[i][0]
        sm += mx - mi - 1
    return sm


assert find(common.Loader.load_lines("test")) == 3
print(f"Lowest IP is {find(common.Loader.load_lines())}")

assert find_all(common.Loader.load_lines("test"), 9) == 2
print(f"Allowed IP count is {find_all(common.Loader.load_lines(), 4294967295)}")


