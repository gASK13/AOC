import common


def run(input, line):
    if line.startswith('swap position'):
        #swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
        (f, s) = sorted([int(line.split(' ')[2]), int(line.split(' ')[5])])
        return input[:f] + input[s] + input[f + 1:s] + input[f] + input[s + 1:]
    elif line.startswith('swap letter'):
        #swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
        (f, s) = sorted([input.index(line.split(' ')[2]), input.index(line.split(' ')[5])])
        return input[:f] + input[s] + input[f + 1:s] + input[f] + input[s + 1:]
    elif line.startswith('rotate based'):
        #rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
        m = input.index(line.split(' ')[6])
        if m >= 4:
            m += 1
        m += 1
        for i in range(m):
            input = input[-1] + input[:-1]
        return input
    elif line.startswith('rotate'):
        # rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
        if line.split(' ')[1] == 'left':
            for i in range(int(line.split(' ')[2])):
                input = input[1:] + input[0]
        else:
            for i in range(int(line.split(' ')[2])):
                input = input[-1] + input[:-1]
        return input
    elif line.startswith('reverse'):
        # reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
        s = int(line.split(' ')[2])
        e = int(line.split(' ')[4]) + 1
        return input[:s] + ''.join(reversed([ch for ch in input[s:e]])) + input[e:]
    elif line.startswith('move'):
        #move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
        f = int(line.split(' ')[2])
        t = int(line.split(' ')[5])
        l = input[f]
        input = input[:f] + input[f+1:]
        return input[:t] + l + input[t:]
    return input

def reverse(input, line):
    if line.startswith('swap position'):
        #swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
        (f, s) = sorted([int(line.split(' ')[2]), int(line.split(' ')[5])])
        return input[:f] + input[s] + input[f + 1:s] + input[f] + input[s + 1:]
    elif line.startswith('swap letter'):
        #swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
        (f, s) = sorted([input.index(line.split(' ')[2]), input.index(line.split(' ')[5])])
        return input[:f] + input[s] + input[f + 1:s] + input[f] + input[s + 1:]
    elif line.startswith('rotate based'):
        #rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
        m = line.split(' ')[6]
        c = -1
        sub = False
        while True:
            input = input[1:] + input[0]
            c += 1
            print(f'{c} -> {input}')
            if c == 5 and not sub:
                c -= 1
                sub = True
            if c == input.index(m):
                break
        return input
    elif line.startswith('rotate'):
        # rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
        if line.split(' ')[1] == 'right':
            for i in range(int(line.split(' ')[2])):
                input = input[1:] + input[0]
        else:
            for i in range(int(line.split(' ')[2])):
                input = input[-1] + input[:-1]
        return input
    elif line.startswith('reverse'):
        # reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
        s = int(line.split(' ')[2])
        e = int(line.split(' ')[4]) + 1
        return input[:s] + ''.join(reversed([ch for ch in input[s:e]])) + input[e:]
    elif line.startswith('move'):
        #move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
        t = int(line.split(' ')[2])
        f = int(line.split(' ')[5])
        l = input[f]
        input = input[:f] + input[f+1:]
        return input[:t] + l + input[t:]
    return input


def run_all(input, lines):
    for line in lines:
        input = run(input, line)
    return input


def reverse_all(input, lines):
    print(input)
    for line in reversed(lines):
        input = reverse(input, line)
        print(line)
        print(input)
    return input


assert run_all('abcde', common.Loader.load_lines('test')) == 'decab'
print(f"Scrambled PWD is {run_all('abcdefgh', common.Loader.load_lines())}")

assert reverse('70123456', 'rotate based on position of letter 0') == '01234567'
assert reverse('01234567', 'rotate based on position of letter 0') == '12345670'
assert reverse('23456701', 'rotate based on position of letter 0') == '23456701'
assert reverse('45670123', 'rotate based on position of letter 0') == '34567012'
assert reverse('67012345', 'rotate based on position of letter 0') == '45670123'
assert reverse('12345670', 'rotate based on position of letter 0') == '56701234'
assert reverse('34567012', 'rotate based on position of letter 0') == '67012345'
assert reverse('56701234', 'rotate based on position of letter 0') == '70123456'

print(f"Unscrambled one is {reverse_all('fbgdceah', common.Loader.load_lines())}")
# NOT defghcba