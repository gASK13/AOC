import common
from colorama import Fore, Back, Style
import tqdm

# assert from test grid
test_data = {(1,1) : 20151125, (1,2) : 18749137, (1,3): 17289845, (3, 4) : 7981243, (5,1) : 77061, (6,6) : 27995004}

def get_diagonal(ord):
    idx = 0
    for i in range(ord):
        idx += i + 1
    return idx

def get_iteration_count(coords):
    ord = coords[0] + coords[1] - 2
    ord = get_diagonal(ord) + coords[1] - 1
    return ord

def iterate(count):
    num = 20151125
    for i in tqdm.tqdm(range(count)):
        num = num * 252533 % 33554393
    return num

def solve(coords):
    return iterate(get_iteration_count(coords))

def parse_input(input):
    return tuple(map(int, input[:-1].split('row ')[1].split(', column ')))

for t in test_data.keys():
    assert solve(t) == test_data[t]

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{solve(parse_input(common.Loader.load_lines()[0]))}')