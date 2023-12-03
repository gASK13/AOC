import common


def peek_around_for_symbol(x, y, matrix):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if 0 <= x + dx < len(matrix[y]) and 0 <= y + dy < len(matrix):
                if matrix[y + dy][x + dx] not in ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return f'{matrix[y+dy][x+dx]}#{dx+x}#{dy+y}'
    return None


def parse_schematic(matrix):
    numbers = {}
    num = 0
    valid_num = None
    for y, line in enumerate(matrix):
        for x, char in enumerate(line):
            if char.isdigit():
                num = num * 10 + int(char)
                if valid_num is None:
                    valid_num = peek_around_for_symbol(x, y, matrix)
            else:
                num, valid_num = store_number(num, numbers, valid_num)
        num, valid_num = store_number(num, numbers, valid_num)
    store_number(num, numbers, valid_num)
    return numbers


def sum_part_numbers(numbers):
    return sum([sum(numbers[key]) for key in numbers])

def store_number(num, numbers, valid_num):
    if num > 0 and valid_num:
        if valid_num not in numbers:
            numbers[valid_num] = []
        numbers[valid_num].append(num)
    num = 0
    valid_num = None
    return num, valid_num


def get_gear_ratio(matrix):
    numbers = parse_schematic(matrix)
    gears = []
    for key in numbers:
        if key.startswith('*#') and len(numbers[key]) == 2:
            gears.append(numbers[key][0] * numbers[key][1])
    return sum(gears)


assert sum_part_numbers(parse_schematic(common.Loader.load_matrix('test'))) == 4361
assert get_gear_ratio(common.Loader.load_matrix('test')) == 467835

#521515
print(f'Sum of numbers is {sum_part_numbers(parse_schematic(common.Loader.load_matrix()))}')
print(f'Gear ratio is {get_gear_ratio(common.Loader.load_matrix())}')