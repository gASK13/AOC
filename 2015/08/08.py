import common
import re

test_data = {'""' : (2, 0, 6),
             '"abc"': (5, 3, 9),
             '"aaa\\"aaa"': (10, 7, 16),
             '"\\x27"': (6, 1, 11)}


def count_chars(line):
    return len(line)


def count_decoded_chars(line):
    # replace using regex \\x[0-9a-f]{2}
    line = line[1:-1].replace("\\\\", "\\").replace("\\\"", "\"")
    line = re.sub(r"\\x[0-9a-f]{2}", "X", line)
    return len(line)


def count_encoded_chars(line):
    return len(line) + 2 + line.count("\\") + line.count("\"")


for t in test_data:
    assert count_chars(t) == test_data[t][0]
    assert count_decoded_chars(t) == test_data[t][1]
    assert count_encoded_chars(t) == test_data[t][2]

print(sum([count_chars(line) - count_decoded_chars(line) for line in common.Loader.load_lines()]))
print(sum([count_encoded_chars(line) - count_chars(line) for line in common.Loader.load_lines()]))