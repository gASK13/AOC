########## PART TWO METHODS ################
# All these position_ functions return WHAT CARD will be at position X after said step
# those are reverse operations so to say


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


########## MAIN CODE ################
# INIT
rules = read_file('22.txt')
poly = parse_rules_into_polynom(rules)

# PART ONE
print('10007 card deck, card 2019 is at position {}'.format((poly[0] * 2019 + poly[1]) % 10007))

# PART TWO, TEST
poly = parse_rules_into_polynom(rules)
size = 119315717514047
turn = 101741582076661
poly = (poly[0] % size, poly[1] % size)
i = 0
while True:
    poly = (poly[0] * poly[0], poly[1] * poly[0] + poly[1])
    poly = (poly[0] % size, poly[1] % size)
    i += 1
    if i % 1000000 == 0:
        print(i)


#X1 = x * a + b
#X2 = x * a^2 + (a+1) * b
#X3 = x * a^3 + (a^2 + a + 1) * b
#X4 = x * a^4 + (a^3 + a^2 + a + 1) * b
#etc....
