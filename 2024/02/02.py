import common

def is_safe_report(report):
    diffs = [report[i+1] - report[i] for i in range(len(report) - 1)]
    if not (all([diff > 0 for diff in diffs]) or all([diff < 0 for diff in diffs])):
        return False
    if not all([4 > abs(diff) > 0 for diff in diffs]):
        return False
    return True

def part_one(reports):
    return sum([1 for report in reports if is_safe_report(report)])


def part_two(reports):
    sum = 0
    for r in reports:
        for ir in [r] + [r[:i] + r[i+1:] for i in range(len(r))]:
            if is_safe_report(ir):
                sum += 1
                break
    return sum

assert is_safe_report([1, 2, 3, 4, 5])
assert is_safe_report([1 ,3, 6, 9, 10])
assert not is_safe_report([1, 5, 7, 8])
assert not is_safe_report([1,2,3,7])
assert not is_safe_report([1, 3, 2])

assert part_one(common.Loader.load_matrix('test', numeric=True, delimiter=' ')) == 2
print(f"Part 1: {part_one(common.Loader.load_matrix(numeric=True, delimiter=' '))}")

assert part_two(common.Loader.load_matrix('test', numeric=True, delimiter=' ')) == 4
print(f"Part 2: {part_two(common.Loader.load_matrix(numeric=True, delimiter=' '))}")