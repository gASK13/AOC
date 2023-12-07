import common
from collections import Counter

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARDS_JOKER = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

test_hands = ['32T3K 765',
              'T55J5 684',
              'KK677 28',
              'KTJJT 220',
              'QQQJA 483']


def rank_hand(counts):
    match counts[0][1]:
        case 5:
            return 6
        case 4:
            return 5
        case 3:
            if counts[1][1] == 2:
                return 4
            return 3
        case 2:
            if counts[1][1] == 2:
                return 2
            return 1
    return 0


def use_joker(counters):
    _cntrs = []
    jokers = 0
    for card, count in counters:
        if card == 'J':
            jokers = count
        else:
            _cntrs.append((card, count))
    if jokers > 0 and len(_cntrs) == 0:
        return [(CARDS[0], jokers)]
    _cntrs[0] = (_cntrs[0][0], _cntrs[0][1] + jokers)
    return _cntrs


class Hand:
    def __init__(self, line):
        self.bid = int(line.split()[1]) if len(line.split()) > 1 else 0
        self.hand = line.split()[0]
        self.rank = 0
        self.rank_joker = 0
        self.compute_rank()
        # TBA - rank hand to stop counting each time

    def __str__(self):
        return f'{self.hand}'

    def __repr__(self):
        return f'{self.hand}'

    def ger_card_rank(self, _cards):
        _r = 0
        for card in self.hand:
            _r *= 100
            _r += _cards.index(card)
        return _r

    def compute_rank(self):
        # first take "rank of hand" (ie straight, full house)
        c = Counter(self.hand)
        self.rank = rank_hand(c.most_common())
        self.rank_joker = rank_hand(use_joker(c.most_common()))

        # add card values
        self.rank *= 10000000000
        self.rank += self.ger_card_rank(CARDS)
        self.rank_joker *= 10000000000
        self.rank_joker += self.ger_card_rank(CARDS_JOKER)


def play_game(hands):
    hands.sort(key=lambda x: x.rank, reverse=False)
    return sum([(i + 1) * h.bid for i, h in enumerate(hands)])


def play_game_joker(hands):
    hands.sort(key=lambda x: x.rank_joker, reverse=False)
    return sum([(i + 1) * h.bid for i, h in enumerate(hands)])


assert Hand('32T3K').rank == 10100080111
assert Hand('T55J5').rank == 30803030903
assert Hand('KK677').rank == 21111040505
assert Hand('KTJJT').rank == 21108090908
assert Hand('QQQJA').rank == 31010100912
assert Hand('AAAAA').rank == 61212121212
assert Hand('QJJQ2').rank == 21009091000
assert Hand('QQQQ2').rank == 51010101000

assert Hand('32T3K').rank_joker == 10201090211
assert Hand('T55J5').rank_joker == 50904040004
assert Hand('KK677').rank_joker == 21111050606
assert Hand('KTJJT').rank_joker == 51109000009
assert Hand('QQQJA').rank_joker == 51010100012
assert Hand('AAAAA').rank_joker == 61212121212
assert Hand('QJJQ2').rank_joker == 51000001001
assert Hand('QQQQ2').rank_joker == 51010101001

assert play_game([Hand(_) for _ in test_hands]) == 6440
assert play_game_joker([Hand(_) for _ in test_hands]) == 5905
print(f'Part 1: {play_game(common.Loader.transform_lines(Hand))}')
print(f'Part 2: {play_game_joker(common.Loader.transform_lines(Hand))}')
