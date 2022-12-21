import common


def step(line):
    switch = {'1': '0', '0': '1'}
    cp = ''.join([switch[c] for c in reversed(line)])
    return line + '0' + cp


def checksum(line):
    group = {'11': '1', '00': '1', '10': '0', '01': '0'}
    while len(line) % 2 == 0:
        line = ''.join([group[line[i * 2:i * 2 + 2]] for i in range(len(line) // 2)])
    return line


def fill(line, length=272):
    while len(line) < length:
        line = step(line)
    return checksum(line[:length])


assert step('1') == '100'
assert step('0') == '001'
assert step('11111') == '11111000000'
assert step('111100001010') == '1111000010100101011110000'
assert step('10000') == '10000011110'
assert step('10000011110') == '10000011110010000111110'

assert checksum('110010110100') == '100'
assert checksum('10000011110010000111') == '01100'

assert fill('10000', 20) == '01100'

print(f'Fill checksum is {fill(common.Loader.load_lines()[0])}')

print(f'Fill checksum of large drive is {fill(common.Loader.load_lines()[0], 35651584)}')