import common

test_data = {
    '{([(<{}[<>[]}>{[]{[(<()>': (1197, 0),
    '[[<[([]))<([[{}[[()]]]': (3, 0),
    '[{[{({}]{}}([{[{{{}}([]': (57, 0),
    '[<(<(<(<{}))><([]([]()': (3, 0),
    '<{([([[(<>()){}]>(<<{{': (25137, 0),
    '[({(<(())[]>[[{[]{<()<>>': (0, 288957),
    '[(()[<>])]({[<{<<[]>>(': (0, 5566),
    '(((({<>}<{<{<>}{[]{[]{}': (0, 1480781),
    '{<[[]]>}<{[{[{[]{()[[[]': (0, 995444),
    '<{([{{}}[<[[[<>{}]]]>[]]': (0, 294)
}

__corruption_scores = {']': 57, '}': 1197, ')': 3, '>': 25137}
__incomplete_scores = {']': 2, '}': 3, ')': 1, '>': 4}


def corruption_score(_line):
    result = parse_line(_line)
    if 'error' in result:
        return __corruption_scores[result['error']]
    return 0


def incomplete_score(_line):
    result = parse_line(_line)
    score = 0
    if 'incomplete' in result:
        for char in reversed(result['incomplete']):
            score *= 5
            score += __incomplete_scores[char]
    return score


def parse_line(_line):
    expected = []
    matches = {'[': ']', '{': '}', '<': '>', '(': ')'}
    for char in _line:
        if char in matches:
            expected.append(matches[char])
        elif char == expected[-1]:
            expected.pop(-1)
        else:
            return {'error':char}
    return {'incomplete': expected}


for t in test_data:
    print('Test for {} - result {} / {} (expected {})'.format(t, corruption_score(t), incomplete_score(t), test_data[t]))

print('Real corruption score {}'.format(sum([corruption_score(line) for line in common.Loader.load_lines()])))
scores = [x for x in sorted([incomplete_score(line) for line in common.Loader.load_lines()]) if x > 0]
print('Real incomplete score {}'.format(scores[len(scores) // 2]))
