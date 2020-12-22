def value_of_deck(_deck):
    _deck.reverse()
    sum = 0
    for (idx, val) in enumerate(_deck):
        sum += (idx + 1) * val
    _deck.reverse()
    return sum


def read_decks(_file):
    players = []
    buffer = []
    for line in open(_file, 'r').readlines():
        if 'Player' in line.strip():
            buffer = []
        elif len(line.strip()) == 0:
            players.append(buffer)
        else:
            buffer.append(int(line))
    players.append(buffer)
    return players


def play_game_simple(_decks):
    while all([len(deck) > 0 for deck in _decks]):
        play_round_simple(_decks)

    _decks.sort(key=lambda d: len(d), reverse=True)
    return _decks[0]


def play_round_simple(_decks):
    _decks.sort(key=lambda d:d[0], reverse=True)
    round = [deck.pop(0) for deck in _decks]
    _decks[0].extend(round)


def hash_decks(_decks):
    return '@'.join(['#'.join([str(card) for card in deck]) for deck in _decks])


def play_game_harder(_decks):
    combinations = {}
    while all([len(deck) > 0 for deck in _decks]):
        hd = hash_decks(_decks)
        if hd in combinations:
            return 0
        combinations[hd] = True
        if all([deck[0] < len(deck) for deck in _decks]):
            winner = play_game_harder([deck[1:1 + deck[0]] for deck in _decks])
            _decks[winner].append(_decks[winner].pop(0))
            _decks[winner].append(_decks[abs(winner - 1)].pop(0))
        else:
            play_round_simple([] + _decks) # copy of decks to avoid switching

    return 0 if len(_decks[0]) > 0 else 1



# PART ONE READY!
decks = read_decks('22.txt')
deck = play_game_simple(decks)
print('Part one ended with {}'.format(value_of_deck(deck)))

# PART TWO READY
decks = read_decks('22.txt')
deck = play_game_harder(decks)
print(decks[deck])
print(value_of_deck(decks[deck]))