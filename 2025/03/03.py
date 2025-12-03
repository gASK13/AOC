import common
from colorama import Fore,Back,Style

def find_highest_joltage(line, digits=2):
    number = 0
    _line = line
    for i in range(digits):
        ti = len(_line)
        digit = 0
        for i in range(len(_line) - (digits - i), -1, -1):
            if int(_line[i]) >= digit:
                ti = i
                digit = int(_line[i])
        number = number * 10 + digit
        _line = _line[ti+1:]
    return number

def part_one(input):
    return sum([find_highest_joltage(line) for line in input])

def part_two(input):
    return sum([find_highest_joltage(line, 12) for line in input])

test_data = {'987654321111111' : 98,
             '111111111111198' : 98,
             '000000010000001' : 11,
             '000000000000000' : 0,
             '000000000000054' : 54,
             '9811' : 98,
             '1198' : 98,
             '9118' : 98,
             '1918' : 98,
             '9181' : 98,
             '9911' : 99}

for t in test_data:
    assert find_highest_joltage(t) == test_data[t]
assert part_one(common.Loader.load_lines('test')) == 357
assert part_two(common.Loader.load_lines('test')) == 3121910778619
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')
