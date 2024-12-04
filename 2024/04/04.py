import common
import re
from colorama import Fore, Back

# this does top right to bottom left (cause it is easier)
def get_diagonals(lines):
    newlines = [[] for _ in range(len(lines)*2)]
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            newlines[y+x].append(char)
    return [''.join(line) for line in newlines]

def search_puzzle(lines, word='XMAS'):
    sum = 0
    # regular left to right
    sum += find_word(lines, word)
    sum += find_word(get_diagonals(lines), word)

    # flip right to left
    lines = [''.join(reversed(line)) for line in lines]
    sum += find_word(lines, word)
    sum += find_word(get_diagonals(lines), word)

    # flip top to bottom
    lines = [''.join(list) for list in common.transpose_matrix(lines)]
    sum += find_word(lines, word)
    sum += find_word(get_diagonals(lines), word)

    # flip bottom to top
    lines = [''.join(reversed(line)) for line in lines]
    sum += find_word(lines, word)
    # one more transpose since the original one led us to same diagonal as before!
    lines = [''.join(list) for list in common.transpose_matrix(lines)]
    sum += find_word(get_diagonals(lines), word)

    return sum

def find_word(lines, word='XMAS'):
    return sum([len(re.findall(word, line)) for line in lines])


assert search_puzzle(common.Loader.load_lines('test_0')) == 0
assert search_puzzle(common.Loader.load_lines('test_4')) == 4
assert search_puzzle(common.Loader.load_lines('test_18')) == 18
assert search_puzzle(common.Loader.load_lines('test_20')) == 20
print(f'Part one: {Fore.BLACK}{Back.GREEN}{search_puzzle(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

###

