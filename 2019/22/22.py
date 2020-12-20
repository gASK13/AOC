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
    deck = [x for x in range(0, _size)]
    for line in _rules:
        if line == 'deal into new stack':
            deck = deal_into_new_stack(deck)
        if 'deal with increment' in line:
            n = int(line.split(' ')[-1])
            deck = deal_with_n(deck, n)
        if 'cut' in line:
            n = int(line.split(' ')[-1])
            deck = cut_n_cards(deck, n)
    return deck


rules = read_file('22.txt')
# PART ONE
deck = shuffle_deck(10007, rules)
print(deck)
for (i, item) in enumerate(deck):
    if item == 2019:
        print(i)


deck = shuffle_deck(119315717514047, rules)