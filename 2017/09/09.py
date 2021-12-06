import common

test_cases = {
    '{}': (1,0),
    '{{{}}}': (6,0),
    '{{},{}}': (5,0),
    '{{{},{},{{}}}}': (16,0),
    '{<a>,<a>,<a>,<a>}': (1,4),
    '{{<ab>},{<ab>},{<ab>},{<ab>}}': (9,8),
    '{{<!!>},{<!!>},{<!!>},{<!!>}}': (9,0),
    '{{<a!>},{<a!>},{<a!>},{<ab>}}': (3,17),
    '<>': (0,0),
    '<random characters>': (0, 17),
    '<<<<>': (0, 3),
    '<{!>}>': (0, 2),
    '<!!>': (0, 0),
    '<!!!>>': (0, 0),
    '<{o"i!a,<{i<a>': (0, 10)
}

def get_score(group):
    score = 0
    current_score = 0
    garbage_count = 0
    ignore = False
    garbage = False
    for char in group:
        if ignore:
            ignore = False
            continue
        if not garbage:
            if char == '{':
                current_score += 1
                score += current_score
                pass
            elif char == '}':
                current_score -= 1
                pass
            elif char == '<':
                garbage = True
                pass
        elif char == '>':
            garbage = False
            pass
        elif char == '!':
            ignore = True
            pass
        else:
            garbage_count += 1
    return score, garbage_count


for test in test_cases:
    print('Case {} has score {} (expected {})'.format(test, get_score(test), test_cases[test]))
    assert get_score(test) == test_cases[test]

print('Real result = {}'.format(get_score(common.Loader.load_lines()[0])))