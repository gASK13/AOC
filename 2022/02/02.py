import common


def translate(item):
    match item:
        case 'A' | 'X':
            return 'R'
        case 'B' | 'Y':
            return 'P'
        case 'C' | 'Z':
            return 'S'


def translate_cplx(item, item2):
    values = ['R', 'P', 'S']
    move = {'X': -1, 'Y' :0, 'Z': 1}
    new_idx = (values.index(translate(item)) + move[item2]) % len(values)
    return values[new_idx]


def outcome(item, item2):
    if item == item2:
        return 3
    if (item == 'R' and item2 == 'P') or (item == 'P' and item2 == 'S') or (item == 'S' and item2 == 'R'):
        return 6
    return 0


def round(items):
    values = {'R': 1, 'P': 2, 'S': 3}
    (item, item2) = [translate(item) for item in items]
    return values[item2] + outcome(item, item2)


def round_cplx(items):
    values = {'R': 1, 'P': 2, 'S': 3}
    (item, item2) = (translate(items[0]), translate_cplx(items[0], items[1]))
    return values[item2] + outcome(item, item2)


assert round(['A', 'Y']) == 8
assert round(['B', 'X']) == 1
assert round(['C', 'Z']) == 6

print(f'Total simple score is {sum([round(items) for items in common.Loader.load_matrix(delimiter=" ")])}')


assert round_cplx(['A', 'Y']) == 4
assert round_cplx(['B', 'X']) == 1
assert round_cplx(['C', 'Z']) == 7

print(f'Total complex score is {sum([round_cplx(items) for items in common.Loader.load_matrix(delimiter=" ")])}')