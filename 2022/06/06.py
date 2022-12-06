import common


def find_marker(line, length=4):
    for i in range(len(line) - length):
        if len(set([c for c in line[i:i+length]])) == length:
            return i + length
    return -1


assert find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert find_marker('nppdvjthqldpwncqszvftbrmjlhg') == 6
assert find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
assert find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

print(f'Marker after {find_marker(common.Loader.load_lines()[0])}')

assert find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
assert find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
assert find_marker('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
assert find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
assert find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26

print(f'Second marker after {find_marker(common.Loader.load_lines()[0], 14)}')