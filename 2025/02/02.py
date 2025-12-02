import common
from colorama import Fore,Back,Style

def check_repeats(start, end, repeats):
    _found = set()
    start_n = int(start)
    end_n = int(end)
    _start = start
    _end = end
    if len(_start) % repeats != 0:
        _start = str(10 ** ((len(_start) // repeats + 1) * repeats - 1))
    if len(_end) % repeats != 0:
        _end = str(10 ** (len(_end) // repeats * repeats) - 1)
    check_start = int(_start[:len(_start) // repeats])
    check_end = int(_end[:len(_end) // repeats])
    for n in range(check_start, check_end + 1):
        check_n = int(str(n) * repeats)
        if start_n <= check_n <= end_n:
            _found.add(check_n)
    return _found

def part_one(range_line):
    found = set()
    for id_range in range_line.split(','):
        start, end = id_range.split('-')
        found = found.union(check_repeats(start, end, 2))
    return sum(found)

def part_two(range_line):
    found = set()
    for id_range in range_line.split(','):
        start, end = id_range.split('-')
        for n in range(2, len(end) + 1):
            found = found.union(check_repeats(start, end, n))
    return sum(found)

assert part_one(common.Loader.load_lines('test')[0]) == 1227775554
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines()[0])}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test')[0]) == 4174379265
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines()[0])}{Style.RESET_ALL}')