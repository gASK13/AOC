########## PART TWO METHODS ################
# All these position_ functions return WHAT CARD will be at position X after said step
# those are reverse operations so to say


def position_into_new_stack(_size, _position):
    return -(_position + 1)


def position_cut_n(_size, _n, _position):
    return _position + _n


def position_deal_n(_size, _n, _position):
    while _position % _n != 0:
        _position += _size
    return _position // _n


def find_source_position(_size, _rules, _position):
    pos = _position
    _rules.reverse()
    for line in _rules:
        if line == 'deal into new stack':
            pos = position_into_new_stack(_size, pos)
        if 'deal with increment' in line:
            n = int(line.split(' ')[-1])
            pos = position_deal_n(_size, n, pos)
        if 'cut' in line:
            n = int(line.split(' ')[-1])
            pos = position_cut_n(_size, n ,pos)
    _rules.reverse()
    return pos % _size


########## PART ONE METHODS ################
# Those are normal operations - they deal with stack of cards and really shuffle it
# This is only optimal for thr first part


def deal_into_new_stack(_stack):
    _stack.reverse()
    return _stack


def cut_n_cards(_stack, _n):
    return _stack[_n:] + _stack[:_n]


def deal_with_n(_stack, _n):
    temp_stack = [x for x in _stack]
    pos = 0
    offset = 0
    for offset_base in range(0, _n):
        for new_pos in range(offset, len(_stack), _n):
            _stack[new_pos] = temp_stack[pos]
            pos += 1
        offset = _n - ((len(_stack) - offset)  % _n)
    return _stack


def read_file(_file_name):
    return [line.strip() for line in open(_file_name, 'r').readlines()]


def shuffle_deck(_size, _rules):
    work_deck = [x for x in range(0, _size)]
    for line in _rules:
        if line == 'deal into new stack':
            work_deck = deal_into_new_stack(work_deck)
        if 'deal with increment' in line:
            n = int(line.split(' ')[-1])
            work_deck = deal_with_n(work_deck, n)
        if 'cut' in line:
            n = int(line.split(' ')[-1])
            work_deck = cut_n_cards(work_deck, n)
    return work_deck


########## MAIN CODE ################
# INIT
rules = read_file('22.txt')

# PART ONE
deck = shuffle_deck(10007, rules)
for (i, item) in enumerate(deck):
    if item == 2019:
        print('10007 card deck, card 2019 is at position {}'.format(i))

# PART TWO, TEST
pos = 2020
step = 0
seen = {2020: 0}
poses = [2020]
while True:
    #size = 80021
    size = 119315717514047
    pos = find_source_position(size, rules, pos)
    poses.append(pos)
    step += 1
    if step % 1000000 == 0:
        print(step)
    if pos in seen:
        print('SEEN {}@{}'.format(step, seen[pos]))
        exit()
    else:
        seen[pos] = step
