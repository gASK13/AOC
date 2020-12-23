class Cup:
    def __init__(self, number):
        self.number = number
        self.next = None


def init_cups(_setup):
    _cups = [Cup(int(c)) for c in _setup]

    for i in range(0, len(_cups)):
        _cups[i - 1].next = _cups[i]

    _current = _cups[0]
    _last = _cups[-1]
    _cups.sort(key=lambda l: l.number)
    return _current, _cups, _last


def move(_cup, _cups):
    nums = [_cup.next.number, _cup.next.next.number, _cup.next.next.next.number]
    first = _cup.next
    last = _cup.next.next.next
    next = _cup.number - 1 if _cup.number > 1 else len(_cups)
    while next in nums:
        next = next - 1 if next > 1 else len(_cups)
    target = _cups[next - 1]
    _cup.next = last.next
    last.next = target.next
    target.next = first
    return _cup.next


def print_cups(cup):
    cur = cup
    print(cur.number, end='>')
    while cur.next != cup:
        cur = cur.next
        print(cur.number, end='>')
    print('')


# PART ONE
#cur, cups, last = init_cups('389125467')
cur, cups, last = init_cups('614752839')

for i in range(0, 100):
    cur = move(cur, cups)
print_cups(cups[0].next)


# PART TWO
cur, cups, last = init_cups('614752839')
#cur, cups, last = init_cups('389125467')
for i in range(len(cups) + 1, 1000001):
    cups.append(Cup(i))
    last.next = cups[-1]
    last = cups[-1]
last.next = cur

for i in range(0, 10000000):
    if (i % 100000 == 0) & (i != 0):
        print(i)
    cur = move(cur, cups)

print('{} > {} > {}'.format(cups[0].number, cups[0].next.number, cups[0].next.next.number))
print(cups[0].next.number * cups[0].next.next.number)
