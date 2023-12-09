import common

test_data = [20, 15, 10, 5, 5]


def fill_jugs(jugs, amount):
    for i in range(len(jugs)):
        if jugs[i] == amount:
            yield [amount]
        elif jugs[i] < amount:
            for j in fill_jugs(jugs[i+1:], amount - jugs[i]):
                yield [jugs[i]] + j


def get_min_count(jugs, amount):
    counts = list(fill_jugs(jugs, amount))
    min_count = min([len(_) for _ in counts])
    return len([_ for _ in counts if len(_) == min_count])

assert len(list(fill_jugs(test_data, 25))) == 4
assert get_min_count(test_data, 25) == 3

print(f'Part 1: {len(list(fill_jugs(common.Loader.load_lines(numeric=True), 150)))}')
print(f'Part 2: {get_min_count(common.Loader.load_lines(numeric=True), 150)}')