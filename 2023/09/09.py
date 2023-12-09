import common

test_data = [([0, 3, 6, 9, 12, 15], 18, -3),
             ([1, 3, 6, 10, 15, 21], 28, 0),
             ([10, 13, 16, 21, 30, 45], 68, 5)]


def get_reading(line):
    if all([_ == 0 for _ in line]):
        return [0] + line + [0]
    subline = [line[i+1] - line[i] for i in range(len(line) - 1)]
    return [line[0] - get_reading(subline)[0]] + line + [line[-1] + get_reading(subline)[-1]]


for data, result, result_back in test_data:
    assert get_reading(data)[-1] == result
    assert get_reading(data)[0] == result_back

assert sum([get_reading(data)[-1] for data, _, _ in test_data]) == 114
assert sum([get_reading(data)[0] for data, _, _ in test_data]) == 2

print(f'Part 1: {sum([get_reading(line)[-1] for line in common.Loader.load_matrix(delimiter=" ", numeric=True)])}')
print(f'Part 2: {sum([get_reading(line)[0] for line in common.Loader.load_matrix(delimiter=" ", numeric=True)])}')

