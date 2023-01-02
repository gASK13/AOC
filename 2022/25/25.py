import common

test = {'1': 1, '2': 2, '1=': 3, '1-': 4, '10': 5, '11': 6, '12': 7,
        '2=': 8, '2-': 9, '20': 10, '1=0': 15, '1-0': 20, '1=11-2': 2022,
        '1-0---0': 12345, '1121-1110-1=0': 314159265, '1=-0-2': 1747, '12111': 906,
        '2=0=': 198, '21': 11, '2=01': 201, '111': 31, '20012': 1257, '112': 32,
        '1=-1=': 353, '1-12': 107, '122': 37, '2=-1=0': 4890}


def snafu(num):
    translate = {0: '=', 1: '-', 2: '0', 3: '1', 4: '2'}
    snf = ''
    while num > 0:
        if num <= 2:
            return str(num) + snf
        else:
            num += 2
            snf = translate[num % 5] + snf
            num //= 5

    return snf

def unsnafu(snf):
    translate = {'=': 0, '-': 1, '0': 2, '1': 3, '2': 4}
    nm = 0
    for (i,c) in enumerate(snf):
        if i == 0:
            nm += int(c)
        else:
            nm *= 5
            nm -= 2
            nm += translate[c]
    return nm


for t in test:
    print(f'{t} => {test[t]} // {unsnafu(t)} // {snafu(test[t])}')
    assert unsnafu(t) == test[t]
    assert snafu(test[t]) == t

print(snafu(sum([unsnafu(line) for line in common.Loader.load_lines()])))
