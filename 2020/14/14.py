#PART ONE
def apply_mask(_mask, _number):
    # _mask = (and, or)
    return (_number & _mask[0]) | _mask[1]


def translate_mask(_mask):
    and_mask = ''
    or_mask = ''
    for char in _mask:
        if char == 'X':
            and_mask += '1'
            or_mask += '0'
        else:
            and_mask += char
            or_mask += char
    return int(and_mask, 2), int(or_mask, 2)


# PART TWO
def expand_mask(_mask):
    # result = (bit_masks)
    # OR mask is 0,X -> KEEP, 1 -> 1
    # AND masks are 0/1 -> 1 (keep), X -> "duplicate" (both 1 and 0)
    two_and_mask = ''
    two_or_mask = ''
    and_masks = []
    or_mask = ''
    x_count = 0
    for char in _mask:
        if char == 'X':
            two_and_mask += 'X'
            two_or_mask += 'X'
            or_mask += '0'
            x_count += 1
        else:
            two_and_mask += '1'
            two_or_mask += '0'
            or_mask += char
    for n in range(0, pow(2, x_count)):
        and_copy = two_and_mask
        or_copy = two_or_mask
        for i in range(0, x_count):
            if n & (1 << i):
                and_copy = and_copy.replace('X', '1', 1)
                or_copy = or_copy.replace('X', '1', 1)
            else:
                and_copy = and_copy.replace('X', '0', 1)
                or_copy = or_copy.replace('X', '0', 1)
        and_masks.append((int(and_copy, 2), int(or_copy, 2)))

    return int(or_mask, 2), and_masks


def apply_masks(_masks, _address):
    address = _masks[0] | _address
    final_addresses = []
    for and_mask, or_mask in _masks[1]:
        final_addresses.append((address & and_mask) | or_mask)
    return final_addresses


mask = (0, 0)
two_mask = ()
mem = {}
two_mem = {}
for line in open('14.txt', 'r').readlines():
    parts = line.strip().split(' = ')
    if parts[0] == 'mask':
        mask = translate_mask(parts[1])
        two_mask = expand_mask(parts[1])
    else:
        value = int(parts[1])
        address = int(parts[0][4:-1])
        mem[address] = apply_mask(mask, value)
        for two_address in apply_masks(two_mask, address):
            two_mem[two_address] = value

#print(mem)
sum = 0
for item in mem.values():
    sum += item
print('SUM #1 is {}'.format(sum))

#print(two_mem)
sum = 0
for item in two_mem.values():
    sum += item
print('SUM #2 is {}'.format(sum))

