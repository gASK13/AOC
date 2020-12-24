# Works by parsing rules into polynom (since the shuffle operations are inversion, addition and multiplication
# Then outputting the resulting A anb B for X*A+B equation


def parse_rules_into_polynom(_rules):
    polynom = (1, 0)
    for line in _rules:
        if line == 'deal into new stack':
            polynom = (-polynom[0], -polynom[1] - 1)
        if 'deal with increment' in line:
            n = int(line.split(' ')[-1])
            polynom = (polynom[0] * n, polynom[1] * n)
        if 'cut' in line:
            n = int(line.split(' ')[-1])
            polynom = (polynom[0], polynom[1] - n)
    return polynom


def read_file(_file_name):
    return [line.strip() for line in open(_file_name, 'r').readlines()]


# Move forward - use power of two to "fast forward" the polynom a bit
# It's a dirty but effective trick!
def move_forward(_x, _turn, _poly, _size):
    x = 1
    poly = _poly
    while x * 2 < _turn:
        poly = (poly[0] * poly[0], poly[1] * poly[0] + poly[1])
        poly = (poly[0] % _size, poly[1] % _size)
        x *= 2

    return (_x * poly[0] + poly[1]) % _size, _turn - x


########## MAIN CODE ################
# INIT
rules = read_file('22.txt')
poly = parse_rules_into_polynom(rules)

# PART ONE
print('10007 card deck, card 2019 is at position {}'.format((poly[0] * 2019 + poly[1]) % 10007))

# PART TWO, IMIT
size = 119315717514047
turn = 101741582076661
poly = (poly[0] % size, poly[1] % size)
print(poly)

# to find what will be at 2020 on TURN, find where 2020 will be on size - turn (-1 cause still not sure why)
t2 = size - turn
t2 -= 1
x = 2020
while t2 > 0:
    x, t2 = move_forward(x, t2, poly, size)
    print(x, t2)

while turn > 0:
    x, turn = move_forward(x, turn, poly, size)
    print(x, turn)
