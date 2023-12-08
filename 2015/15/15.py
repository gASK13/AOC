import common
import tqdm

ingredient = ['Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8',
              'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3']


def parse_line(line):
    parts = line.split(' ')
    return [int(parts[2][:-1]), int(parts[4][:-1]), int(parts[6][:-1]), int(parts[8][:-1]), int(parts[10])]


def get_amounts(number_of_ingredients, total=100):
    if number_of_ingredients == 1:
        yield [total]
    else:
        for i in range(0, total + 1):
            for a in get_amounts(number_of_ingredients - 1, total - i):
                yield [i] + a


def score(ingredients, amounts, calory_limit=None):
    _sum = [0, 0, 0, 0, 0]
    for i in range(len(ingredients)):
        for j in range(5):
            _sum[j] += ingredients[i][j] * amounts[i]
    if calory_limit is not None and _sum[4] != calory_limit:
        return 0
    if any([_ <= 0 for _ in _sum]):
        return 0
    return max(0, _sum[0]) * max(0, _sum[1]) * max(0, _sum[2]) * max(0, _sum[3])


assert score([parse_line(_) for _ in ingredient], [44, 56]) == 62842880
assert max([score([parse_line(_) for _ in ingredient], a) for a in get_amounts(2)]) == 62842880
assert max([score([parse_line(_) for _ in ingredient], a, 500) for a in get_amounts(2)]) == 57600000

total = len(list(get_amounts(4)))
ingredients = [parse_line(_) for _ in common.Loader.load_lines()]
print(f'Part 1: {max([score(ingredients, a) for a in tqdm.tqdm(get_amounts(4), total = total)])}')
print(f'Part 2: {max([score(ingredients, a, 500) for a in tqdm.tqdm(get_amounts(4), total = total)])}')
