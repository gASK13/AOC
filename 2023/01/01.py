import common

number_texts = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def compute_number(input_line, text=False):
    if text:
        return find_first_number_in_line_text(input_line) * 10 + find_last_number_in_line_text(input_line)
    else:
        return find_first_number_in_line(input_line) * 10 + find_last_number_in_line(input_line)


def find_first_number_in_line(input_line):
    for i in range(len(input_line)):
        if input_line[i].isdigit():
            return int(input_line[i])
    return 0


def find_last_number_in_line(input_line):
    return find_first_number_in_line(input_line[::-1])


def find_first_number_in_line_text(input_line):
    for i in range(len(input_line)):
        if input_line[i].isdigit():
            return int(input_line[i])
        for (j, number) in enumerate(number_texts):
            if input_line[i:i + len(number)] == number:
                return j
    return 0


def find_last_number_in_line_text(input_line):
    for i in range(len(input_line)):
        if input_line[-i - 1].isdigit():
            return int(input_line[-i - 1])
        for (j, number) in enumerate(number_texts):
            if -i == 0:
                if input_line[-i - len(number):] == number:
                    return j
            elif input_line[-i - len(number):-i] == number:
                return j
    return 0


test_data = {
    '1abc2': (12, 12),
    'pqr3stu8vwx': (38, 38),
    'a1b2c3d4e5f': (15, 15),
    'treb7uchet': (77, 77),
    'two1nine': (11, 29),
    'eightwothree': (0, 83),
    'abcone2threexyz': (22, 13),
    'xtwone3four': (33, 24),
    '4nineeightseven2': (42, 42),
    'zoneight234': (24, 14),
    '7pqrstsixteen': (77, 76)
}

for line, (res, res_text) in test_data.items():
    print(f'Line {line} should be {res} and is {compute_number(line)}')
    assert compute_number(line, False) == res
    print(f'Line {line} should be {res_text} and is {compute_number(line, True)}')
    assert compute_number(line, True) == res_text

print(f'Calibration value is {sum([compute_number(line) for line in common.Loader.load_lines()])}')
print(f'Calibration value is {sum([compute_number(line, True) for line in common.Loader.load_lines()])}')
