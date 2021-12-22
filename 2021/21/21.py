class Die:
    def __init__(self, sides):
        self.__sides = sides
        self.__next = 1

    def roll(self):
        n = self.__next
        self.__next += 1
        if self.__next > self.__sides:
            self.__next = 1
        return n


def run_game(p1, p2):
    rolls = 0
    players = [[p1, 0], [p2, 0]]
    die = Die(100)
    roll_count = 3
    while all([s < 1000 for p, s in players]):
        player = players[rolls % len(players)]
        rolls += roll_count
        three_rolls = sum([die.roll() for i in range(roll_count)])
        player[0] = (player[0] + three_rolls) % 10
        player[1] += player[0] if player[0] != 0 else 10
    print(rolls)
    print(players)
    return rolls * sum([s for p, s in players if s < 1000])


def dirac_dice_distribution():
    return [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]


def get_min_state(states):
    min_key = None
    for key in states:
        if min_key is None:
            min_key = key
        if min_key[1] + min_key[3] > key[1] + key[3]:
            min_key = key
    return min_key


def run_game_dirac(p1, p2):
    # I need to reach 21
    # I can do it by being on various states
    # How many steps will it take for each state (3-9)?
    # compare to other and find how often is it "less"?
    wins = [0, 0]
    states = {(p1, 0, p2, 0, 0): 1}
    while len(states) > 0:
        state = get_min_state(states)
        state_count = states.pop(state)
        for roll, count in dirac_dice_distribution():
            new_state = (state[0 + state[4] * 2] + roll) % 10
            score = state[1 + state[4] * 2] + (new_state if new_state > 0 else 10)
            if score >= 21:
                wins[state[4]] += count * state_count
            else:
                if state[4] == 1:
                    new_key = (state[0], state[1], new_state, score, 0)
                else:
                    new_key = (new_state, score, state[2], state[3], 1)
                if new_key not in states:
                    states[new_key] = 0
                states[new_key] += state_count * count
        print(len(states))
        print(wins)
    print(wins)
    return max(wins)


print(f'Test {run_game(4,8)} - expected 745 * 993 = 739785')
print(f'Real {run_game(2,7)}')


print(f'Test {run_game_dirac(4,8)} - expected 444356092776315')
print(f'Real {run_game_dirac(2,7)}')
