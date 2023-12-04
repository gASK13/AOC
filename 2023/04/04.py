import common

test_data = {'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53': 8,
             'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19': 2,
             'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1': 2,
             'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83': 1,
             'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36': 0,
             'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11': 0}


class Card:
    def __init__(self, line):
        self.number = line.split(':')[0].split(' ')[1]
        self.draw = [int(n) for n in line.split(': ')[1].split(' | ')[1].split()]
        self.winners = [int(n) for n in line.split(': ')[1].split(' | ')[0].split()]

    def points(self):
        retval = 0
        for n in self.draw:
            if n in self.winners:
                if retval == 0:
                    retval = 1
                else:
                    retval *= 2
        return retval

    def card_count(self):
        return sum([1 for n in self.draw if n in self.winners])


def second_game(cards):
    multiplier = [1 for c in cards]
    for i in range(len(cards)):
        for j in range(cards[i].card_count()):
            multiplier[i+j+1] += multiplier[i]
    return sum(multiplier)


for t in test_data:
    assert Card(t).points() == test_data[t]

assert second_game([Card(t) for t in test_data]) == 30

print(f'Total points {sum([c.points() for c in common.Loader.transform_lines(Card)])}')
print(f'Total multiplied second game points {second_game(common.Loader.transform_lines(Card))}')
