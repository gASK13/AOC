import common

test = ['Time:      7  15   30', 'Distance:  9  40  200']

def parse_races(lines):
    return common.utils.transpose_matrix([[int(_) for _ in line.split()[1:]] for line in lines])


def parse_one_race(lines):
    return [int(lines[0][5:].replace(' ', '')), int(lines[1][9:].replace(' ', ''))]


def find_wins(race):
    time, distance = race
    wins = 0
    for i in range(time):
        if (time-i) * i > distance:
            wins += 1
    return wins


def find_margin(races):
    product = 1
    for race in races:
        product *= find_wins(race)
    return product


assert find_wins(parse_races(test)[0]) == 4
assert find_wins(parse_races(test)[1]) == 8
assert find_wins(parse_races(test)[2]) == 9
assert find_margin(parse_races(test)) == 4 * 8 * 9
assert find_wins(parse_one_race(test)) == 71503

print(f'Part 1: {find_margin(parse_races(common.Loader.load_lines()))}')
print(f'Part 2: {find_wins(parse_one_race(common.Loader.load_lines()))}')
