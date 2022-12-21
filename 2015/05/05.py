import common
from collections import Counter

def is_nice_string(line):
    if 'ab' in line or 'cd' in line or 'pq' in line or 'xy' in line:
        return False
    c = Counter(line)
    if c['a'] + c['e'] + c['i'] + c['o'] + c['u'] < 3:
        return False
    return any([line[i] == line[i+1] for i in range(len(line) - 1)])


def is_nice_new_model(line):
    if not any([line[i] == line[i + 2] for i in range(len(line) - 2)]):
        return False
    for i in range(len(line) - 1):
        segment = line[i:i+2]
        if segment in line[i+2:]:
            return True
    return False


assert is_nice_string('ugknbfddgicrmopn')
assert is_nice_string('aaa')
assert not is_nice_string('jchzalrnumimnmhp')
assert not is_nice_string('haegwjzuvuyypxyu')
assert not is_nice_string('dvszwmarrgswjxmb')

print(f'Nice string count is {sum([1 for x in common.Loader.load_lines() if is_nice_string(x)])}')

assert is_nice_new_model('qjhvhtzxzqqjkmpb')
assert is_nice_new_model('xxyxx')
assert not is_nice_new_model('uurcxstgmygtbstg')
assert not is_nice_new_model('ieodomkazucvgmuy')

print(f'Nice string count is {sum([1 for x in common.Loader.load_lines() if is_nice_new_model(x)])}')