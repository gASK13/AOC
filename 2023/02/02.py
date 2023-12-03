import common

test_data = {'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green': (True, 48),
             'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue': (True, 12),
             'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red': (False, 1560),
             'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red': (False, 630),
             'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green': (True, 36)}


def split_game(line):
    return int(line.split(': ')[0].split(' ')[1]), line.split(': ')[1].split('; ')


def is_possible(attempts, setup={'red': 12, 'green': 13, 'blue': 14}):
    for attempt in attempts:
        for value, color in extract_colors(attempt):
            if setup[color] < value:
                return False
    return True


def extract_colors(attempt):
    return [(int(item.split(' ')[0]), item.split(' ')[1]) for item in attempt.split(', ')]


def smallest_power(attempts):
    colors = {'red': 0, 'green': 0, 'blue': 0}
    for attempt in attempts:
        for value, color in extract_colors(attempt):
            colors[color] = max(colors[color], value)
    return colors['red'] * colors['green'] * colors['blue']


for line, res in test_data.items():
    assert is_possible(split_game(line)[1]) == res[0]
    assert smallest_power(split_game(line)[1]) == res[1]

sum = 0
sum_power = 0
for game, attempts in [split_game(line) for line in common.Loader.load_lines()]:
    if is_possible(attempts):
        sum += game
    sum_power += smallest_power(attempts)

print(f'Sum of possible games is {sum}')
print(f'Sum of lowest powers is {sum_power}')
