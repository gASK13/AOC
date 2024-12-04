import common
import re
from colorama import Fore, Back

# this does top right to bottom left (cause it is easier)
def get_diagonals(lines):
    # if not square, fill it
    if len(lines) > len(lines[0]):
        lines = [line + '.' * (len(lines) - len(line)) for line in lines]
    if len(lines) < len(lines[0]):
        lines += ['.' * len(lines[0]) for _ in range(len(lines[0]) - len(lines))]

    newlines = [[] for _ in range(len(lines)*2)]
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            newlines[y+x].append(char)
    # for the second part we do this magic:
    # - split into two lists - even count and odd count
    # - fill both to "same length" with '.' character so the original is in the middle
    # - then join them with empty line in between
    even = pad_strings([''.join(line) for idx, line in enumerate(newlines) if idx % 2 == 0])
    odd = pad_strings([''.join(line) for idx, line in enumerate(newlines) if idx % 2 == 1])
    return even + [''.join(['_' for _ in range(len(even))])] + odd

def pad_strings(lines):
    maxlen = max([len(line) for line in lines])
    newlines = []
    for line in lines:
        assert (len(line) - maxlen) % 2 == 0
        pad = '.' * ((maxlen - len(line)) // 2)
        newlines.append(pad + line + pad)
    return newlines

def find_word(x, y, lines):
    # horizontal!
    return sum([lines[y][x-2:x+2] == 'XMAS',
                lines[y][x - 1:x + 3] == 'SAMX',
                (len(lines) - 2) > y > 0 and lines[y+2][x] == 'X' and lines[y+1][x] == 'M' and lines[y-1][x] == 'S',
                (len(lines) - 1) > y > 1 and lines[y-2][x] == 'X' and lines[y-1][x] == 'M' and lines[y+1][x] == 'S'])

def find_cross(x, y, lines):
    # find MAS in all directions
    if (len(lines) - 1) > y > 0:
        if lines[y][x-1:x+2] in ['MAS', 'SAM'] and ''.join([lines[y-1][x], lines[y][x], lines[y+1][x]]) in ['MAS', 'SAM']:
            return 1
    return 0

def part_one(lines):
    return search_field(find_word, lines) + search_field(find_word, get_diagonals(lines))

def part_two(lines):
    return search_field(find_cross, get_diagonals(lines))

def search_field(finder, lines):
    _sum = 0
    for idy, line in enumerate(lines):
        for idx, char in enumerate(line):
            if char == 'A':
                _sum += finder(idx, idy, lines)
    return _sum


assert part_one(common.Loader.load_lines('test_0')) == 0
assert part_one(common.Loader.load_lines('test_4')) == 4
assert part_one(common.Loader.load_lines('test_18')) == 18
assert part_one(common.Loader.load_lines('test_20')) == 20
print(f'Part one: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

assert part_two(common.Loader.load_lines('test_0')) == 0
assert part_two(common.Loader.load_lines('test_4')) == 0
assert part_two(common.Loader.load_lines('test_20')) == 0
assert part_two(common.Loader.load_lines('test_18')) == 9
print(f'Part two: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')
# 1934 too high!

