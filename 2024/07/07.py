import common
from colorama import Fore, Back

def is_valid(line, concat = False):
    result = int(line.split(':')[0])
    values = [int(x) for x in line.split(': ')[1].split(' ')]
    if rec_compute(result, values, concat):
        print(Fore.GREEN + f'{result} is valid' + Fore.RESET)
        return result
    else:
        print(Fore.RED + f'{result} is invalid' + Fore.RESET)
        return 0

def rec_compute(result, values, concat):
    if len(values) == 1:
        if values[0] == result:
            return True
        return False

    if not concat:
        return rec_compute(result, [values[0] + values[1]] + values[2:], concat) or rec_compute(result, [values[0] * values[1]] + values[2:], concat)
    return (rec_compute(result, [values[0] + values[1]] + values[2:], concat)
            or rec_compute(result,[values[0] * values[1]] + values[2:], concat)
            or rec_compute(result, [values[0] * pow(10, len(str(values[1]))) + values[1]] + values[2:], concat))



def part_one(lines):
    return sum([is_valid(line) for line in lines])


def part_two(lines):
    return sum([is_valid(line, True) for line in lines])

assert part_one(common.Loader.load_lines("test")) == 3749
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')

assert part_two(common.Loader.load_lines("test")) == 11387
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Fore.RESET}{Back.RESET}')