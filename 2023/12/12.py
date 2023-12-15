import common
import regex
from colorama import Fore, Back, Style
import tqdm

test_data = {
    '???#??# 2,2': 1,
    '??#????#?? 3,1,1': 6,
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


def run_tests():
    fails = 0
    for line, expected in test_data.items():
        solved = Springs(line).solve()
        if solved != expected:
            print(f'{Fore.RED}{line} not matching!: {solved}/{expected}')
            fails += 1
    for line, expected in test_data_unfolded.items():
        solved = Springs(line, True).solve()
        if solved != expected:
            print(f'{Fore.RED}{line} not matching for expanded!: {solved}/{expected}')
            fails += 1
    if fails > 0:
        print(f'{Back.RED}{Fore.BLACK}{fails} tests failed, stopping!')
        exit(1)


class Springs:
    def __init__(self, line=None, unfold=False, count=1):
        self.line = line
        self.map = line.split(' ')[0]
        self.count = count
        self.groups = [int(_) for _ in line.split(' ')[1].split(',')] if line.split(' ')[1] != '' else []

        if unfold:
            self.map = '?'.join([self.map for _ in range(5)])
            self.groups = [item for sublist in [self.groups for _ in range(5)] for item in sublist]

        self.map.strip('.')
        self.line = f'{self.map} {",".join([str(_) for _ in self.groups])}'

    def __str__(self):
        return self.line

    def __repr__(self):
        return self.__str__()

    def solve(self):
        # try to generate all possible placements of groups and validate each
        return self.generate_placements()

    def is_valid(self, placement):
        for i in range(len(placement)):
            if placement[i] == '#' and self.map[i] == '.':
                return 0
            if placement[i] == '.' and self.map[i] == '#':
                return 0

        return 1

    def generate_placements(self):
        if self.line in SEEN:
            return SEEN[self.line]
        g = self.groups[0]
        diff = len(self.map) - sum(self.groups[1:]) - len(self.groups[1:])
        if diff < g:
            return []
        vals = 0
        for i in range(diff - g + 1):
            if len(self.groups) == 1:
                if '.' in self.map[i:i + g] or '#' in self.map[i + g:] or '#' in self.map[:i]:
                    continue
                vals += 1
            else:
                if '.' in self.map[i:i + g] or '#' in self.map[i + g:i + g + 1] or '#' in self.map[:i]:
                    continue
                vals += Springs(self.map[i + g + 1:] + ' ' + ','.join([str(_) for _ in self.groups[1:]])).generate_placements()

        SEEN[self.line] = vals
        return vals


# global cache to avoid recomputing what we saw
SEEN = {}

run_tests()

print(f'\nPart 1: {Back.GREEN}{Fore.BLACK}{sum([Springs(_).solve() for _ in common.Loader.load_lines()])}')

# Looks good, does not work - too slow :O
print(f'\nPart 2: {Back.GREEN}{Fore.BLACK}{sum([Springs(_, True).solve() for _ in tqdm.tqdm(common.Loader.load_lines())])}')
