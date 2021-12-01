from common.loader import Loader


def is_valid(_pass_array):
    return len(_pass_array) == len(set(_pass_array))


def is_valid_v2(_pass_array):
    return len(_pass_array) == len(set(["".join(sorted(list(x))) for x in _pass_array]))


print(is_valid('aa bb cc dd ee'.split(' ')))
print(is_valid('aa bb cc dd aa'.split(' ')))
print(is_valid('aa bb cc dd aaa'.split(' ')))

mat = Loader.load_matrix('input.txt', delimiter='\\s+')

print(sum([1 if is_valid(x) else 0 for x in mat]))

print("PART TWO")
print(is_valid_v2('abcde fghij'.split(' ')))
print(is_valid_v2('abcde xyz ecdab'.split(' ')))
print(is_valid_v2('a ab abc abd abf abj'.split(' ')))
print(is_valid_v2('iiii oiii ooii oooi oooo'.split(' ')))
print(is_valid_v2('oiii ioii iioi iiio'.split(' ')))

print(sum([1 if is_valid_v2(x) else 0 for x in mat]))