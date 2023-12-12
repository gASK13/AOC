import common
import regex
from colorama import Fore, Back, Style
import tqdm

test_data = {
    '???.### 1,1,3': 1,
    '.??..??...?##. 1,1,3': 4,
    '?#?#?#?#?#?#?#? 1,3,1,6': 1,
    '????.#...#... 4,1,1': 1,
    '????.######..#####. 1,6,5': 4,
    '?###???????? 3,2,1': 10,
    '????.????? 1,1,1': 40,
    '???#..? 1,1': 3,
    '?????#..?.? 1,1,1': 12,
    '???#??? 3': 3,
    '?#??...? 3': 2,
    '?#?#?#? 1,3': 1,
    '?###???? 3,1': 3,
    '??? 1': 3,
    '?????????? 1,1,1,1': 35,
    '???????????? 1,1,1,1,1': 56,
    '???????????? 1,1,2,1,1': 21,
    '?.?.??.??? 1,3': 4,
    '?#?#??##?#?#???.?#?. 5,6,2': 2,
    '?????#?..?#? 2,2,2': 10,
    '???#???#.#??#??##?? 1,1,1,1,9': 2}

test_data_unfolded = {
    '???.### 1,1,3': 1,
    '.??..??...?##. 1,1,3': 16384,
    '?#?#?#?#?#?#?#? 1,3,1,6': 1,
    '????.#...#... 4,1,1': 16,
    '????.######..#####. 1,6,5': 2500,
    '?###???????? 3,2,1': 506250
}

MATCH_QMARKS = regex.compile(r'^(\?+)(\.|$)')
MATCH_HASHES = regex.compile(r'^(#+)(\.|$)')

def run_tests():
    fails = 0
    for line, expected in test_data.items():
        solved = solve(line)
        if solved != expected:
            print(f'{Fore.RED}{line} not matching!: {solved}/{expected}')
            fails += 1
    for line, expected in test_data_unfolded.items():
        print(f'{Fore.YELLOW}Testing {line}...')
        solved = solve(line, True)
        if solved != expected:
            print(f'{Fore.RED}{line} not matching for expanded!: {solved}/{expected}')
            fails += 1
    if fails > 0:
        print(f'{Back.RED}{Fore.BLACK}{fails} tests failed, stopping!')
        exit(1)


def count_ways(group_idx, space_diff):
    match group_idx:
        case 0:
            return 1
        case 1:
            return space_diff + 1
        case 2:
            return (space_diff + 1) * (space_diff + 2) // 2
        case 3:
            return (space_diff + 1) * (space_diff + 2) * (space_diff + 3) // 6
        case 4:
            return (space_diff + 1) * (space_diff + 2) * (space_diff + 3) * (space_diff + 4) // 24
        case 5:
            return (space_diff + 1) * (space_diff + 2) * (space_diff + 3) * (space_diff + 4) * (space_diff + 5) // 120
    raise f'Invalid group_idx {group_idx}'


class Springs:
    def __init__(self, line=None, unfold=False, count=1):
        self.line = line
        self.map = line.split(' ')[0]
        self.count = count
        self.groups = [int(_) for _ in line.split(' ')[1].split(',')] if line.split(' ')[1] != '' else []

        if unfold:
            self.map = '?'.join([self.map for _ in range(5)])
            self.groups = [item for sublist in [self.groups for _ in range(5)] for item in sublist]
            self.line = f'{self.map} {",".join([str(_) for _ in self.groups])}'

    def is_done(self):
        return len(self.groups) == 0 and (not '#' in self.map)

    def __str__(self):
        return self.line

    def __repr__(self):
        return self.__str__()

    def fill_next(self):
        # strip any leading . (dots) as we don't need those
        self.map = self.map.lstrip('.')

        # If we have no groups or no map and we're not "done", we can't continue
        if self.groups == [] or len(self.map) == 0:
            return {}

        # set of return values
        retval = {}

        # If next part is ???., then try to fill in all possible combos
        qmatches = MATCH_QMARKS.match(self.map)
        if qmatches is not None:
            count = len(qmatches[1])
            # how many can I fit in?
            for i in range(len(self.groups)):
                diff = count - sum(self.groups[:i + 1]) - i
                if diff >= 0:
                    new_spring = f'{self.map[count:]} {",".join([str(_) for _ in self.groups[i + 1:]])}'
                    if new_spring in retval:
                        retval[new_spring] += count_ways(i + 1, diff)
                    else:
                        retval[new_spring] = count_ways(i + 1, diff)
                else:
                    # we can't fit no more
                    break

            # also try to not fill in ANY groups
            new_spring = f'{self.map[count:]} {",".join([str(_) for _ in self.groups])}'
            if new_spring in retval:
                retval[new_spring] += 1
            else:
                retval[new_spring] = 1

        # If next part is ###., then try to match or fail
        else:
            hcount = MATCH_HASHES.match(self.map)
            if hcount is not None:
                if len(hcount[1]) == self.groups[0]:
                    new_spring = f'{self.map[self.groups[0]:]} {",".join([str(_) for _ in self.groups[1:]])}'
                    if new_spring in retval:
                        retval[new_spring] += 1
                    else:
                        retval[new_spring] = 1

            # If next part is #?#., then try to fill in all possible combos
            else:
                # find index of first # as anchor to fill on
                first_hash = self.map.index('#')

                for gi in range(len(self.groups)):
                    # let's use first group to first # in all the ways we can
                    group = self.groups[gi]

                    # try to fit it in all the ways on the anchor
                    for i in range(group):
                        left_length = group - i - 1
                        left_space = first_hash - left_length - 1

                        # check if "previous" groups will fit in
                        diff = left_space - sum(self.groups[:gi]) - (gi - 1)
                        if gi > 0 and diff < 0:
                            continue

                        # check if the group will fit on left
                        if left_length > first_hash:
                            continue
                        # check if there is enough space on the right
                        if len(self.map) < first_hash + 1 + i or '.' in self.map[first_hash + 1:first_hash + 1 + i]:
                            continue
                        # check if there is separation on the right
                        if first_hash + i + 1 < len(self.map) and self.map[first_hash + i + 1] == '#':
                            continue

                        # add to options
                        new_spring = f'{self.map[first_hash + 2 + i:]} {",".join([str(_) for _ in self.groups[gi + 1:]])}'
                        if new_spring in retval:
                            retval[new_spring] += count_ways(gi, diff)
                        else:
                            retval[new_spring] = count_ways(gi, diff)

        return retval


def solve(_line, unfolded=False):
    springs = [Springs(_line, unfolded)]
    seen = {}
    total = 0
    while len(springs) > 0:
        spring = springs.pop()
        if spring.is_done():
            total += spring.count
        else:
            if spring not in seen:
                seen[spring] = spring.fill_next()
            for new_spring, new_count in seen[spring].items():
                springs.append(Springs(line=new_spring, count=new_count*spring.count))

    return total


run_tests()

print(f'\nPart 1: {Back.GREEN}{Fore.BLACK}{sum([solve(_) for _ in common.Loader.load_lines()])}')

# Looks good, does not work - too slow :O
print(f'\nPart 2: {Back.GREEN}{Fore.BLACK}{sum([solve(_, True) for _ in tqdm.tqdm(common.Loader.load_lines())])}')