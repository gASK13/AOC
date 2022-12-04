import common


def convert_to_set(item):
    (lower, upper) = [int(i) for i in item.split('-')]
    return set([i for i in range(lower, upper+1)])


def is_pair_included(pair):
    (elf1, elf2) = [convert_to_set(i) for i in pair]
    if elf1.issubset(elf2) or elf2.issubset(elf1):
        return True
    return False


def do_pairs_overlap(pair):
    (elf1, elf2) = [convert_to_set(i) for i in pair]
    if len(elf1.intersection(elf2)) > 0:
        return True
    return False


assert not is_pair_included(['2-4','6-8'])
assert not is_pair_included(['2-3','4-5'])
assert not is_pair_included(['5-7','7-9'])
assert is_pair_included(['2-8','3-7'])
assert is_pair_included(['6-6','4-6'])
assert not is_pair_included(['2-6','4-8'])

print(f'The count of fully overlaping elves is {sum([1 if is_pair_included(x) else 0 for x in common.Loader.load_matrix(delimiter=",")])}')

assert not do_pairs_overlap(['2-4','6-8'])
assert not do_pairs_overlap(['2-3','4-5'])
assert do_pairs_overlap(['5-7','7-9'])
assert do_pairs_overlap(['2-8','3-7'])
assert do_pairs_overlap(['6-6','4-6'])
assert do_pairs_overlap(['2-6','4-8'])

print(f'The count of partially overlapping elves is {sum([1 if do_pairs_overlap(x) else 0 for x in common.Loader.load_matrix(delimiter=",")])}')