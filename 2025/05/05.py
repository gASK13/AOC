import common
from colorama import Fore, Back, Style

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

def build_ranges(range_lines):
    ranges = []
    for line in range_lines:
        mi, mx = [int(l) for l in line.split('-')]
        # the ranges will be "distinct" so I can assuem that min of next is > then max of last
        # so I can iterate and find one where my min < his max and then update his max and "eat the rest" if needed
        ranges = merge_ranges(ranges, (mi, mx))

    return ranges

def part_one(lines):
    ranges = build_ranges(lines[:lines.index('')])
    ingredients = lines[lines.index('')+1:]
    cnt = 0
    for i in ingredients:
        for ri, rx in ranges:
            if ri <= int(i) <= rx:
                cnt +=1
                break
    return cnt


def part_two(lines):
    ranges = build_ranges(lines[:lines.index('')])
    return sum([rx - ri + 1 for ri,rx in ranges])


assert part_one(common.Loader.load_lines('test')) == 3
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test')) == 14
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')