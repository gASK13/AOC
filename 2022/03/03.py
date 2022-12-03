import common


def find_badge(lines):
    res = None
    for i in range(3):
        if res is None:
            res = set([c for c in lines.pop()])
        else:
            res = res.intersection(set([c for c in lines.pop()]))
    assert len(res) == 1
    return res.pop()


def find_item(line):
    if len(line) % 2 == 1:
        raise 'OOPS'
    c1 = set([c for c in line[:len(line)//2]])
    c2 = set([c for c in line[len(line)//2:]])
    assert len(c1.intersection(c2)) == 1
    return c1.intersection(c2).pop()


def item_value(item):
    if 96 < ord(item) < 123:
        return ord(item) - 96
    return ord(item) - 64 + 26


assert find_item('vJrwpWtwJgWrhcsFMMfFFhFp') == 'p'
assert find_item('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL') == 'L'
assert find_item('PmmdzqPrVvPwwTWBwg') == 'P'
assert find_item('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn') == 'v'
assert find_item('ttgJtRGJQctTZtZT') == 't'
assert find_item('CrZsJsPPZsGzwwsLwLmpwMDw') == 's'


assert item_value(find_item('vJrwpWtwJgWrhcsFMMfFFhFp')) == 16
assert item_value(find_item('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')) == 38
assert item_value(find_item('PmmdzqPrVvPwwTWBwg')) == 42
assert item_value(find_item('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn')) ==22
assert item_value(find_item('ttgJtRGJQctTZtZT')) == 20
assert item_value(find_item('CrZsJsPPZsGzwwsLwLmpwMDw')) == 19

print(f'Sum of values in input is {sum([item_value(find_item(line)) for line in common.Loader.load_lines()])}')

assert find_badge(['vJrwpWtwJgWrhcsFMMfFFhFp','jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL','PmmdzqPrVvPwwTWBwg']) == 'r'
assert find_badge(['wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'ttgJtRGJQctTZtZT', 'CrZsJsPPZsGzwwsLwLmpwMDw']) == 'Z'

assert item_value(find_badge(['vJrwpWtwJgWrhcsFMMfFFhFp','jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL','PmmdzqPrVvPwwTWBwg'])) == 18
assert item_value(find_badge(['wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'ttgJtRGJQctTZtZT', 'CrZsJsPPZsGzwwsLwLmpwMDw'])) == 52

lines = common.Loader.load_lines()
value = 0
while len(lines) > 0:
    value += item_value(find_badge(lines))
print(f'Sum of values in badges is {value}')