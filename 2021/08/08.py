import common

test_data = {
    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe': 8394,
    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc': 9781,
    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg': 1197,
    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb': 9361,
    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea': 4873,
    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb': 8418,
    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe': 4548,
    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef': 1625,
    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb': 8717,
    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce': 4315
}


def count_1478(line):
    data = line.split(' | ')[1].split(' ')
    return sum([1 for item in data if len(item) == 2 or len(item) == 3 or len(item) == 4 or len(item) == 7])


def decode_line(line):
    # prepare and sort data
    training = set(
        [''.join(sorted(item)) for item in line.split(' | ')[0].split(' ') + line.split(' | ')[1].split(' ')])
    data = [''.join(sorted(item)) for item in line.split(' | ')[1].split(' ')]

    # translate "easy ones"
    translate = {[item for item in training if len(item) == 2][0]: 1,
                 [item for item in training if len(item) == 3][0]: 7,
                 [item for item in training if len(item) == 4][0]: 4,
                 [item for item in training if len(item) == 7][0]: 8}

    # store helper subsets
    cf = [item for item in training if len(item) == 2][0]
    a = ''.join([i for i in [item for item in training if len(item) == 3][0] if i not in cf])
    bd = ''.join([i for i in [item for item in training if len(item) == 4][0] if i not in cf])

    # decode 5 lengths
    for item in [item for item in training if len(item) == 5]:
        if all([x in item for x in cf]):
            translate[item] = 3
        elif all([x in item for x in bd]):
            translate[item] = 5
        else:
            translate[item] = 2

    # decode 5 lengths
    for item in [item for item in training if len(item) == 6]:
        if any([x not in item for x in cf]):
            translate[item] = 6
        elif any([x not in item for x in bd]):
            translate[item] = 0
        else:
            translate[item] = 9
    return int(''.join([str(translate[d]) for d in data]))


print('PART ONE:')
print('{}, expected {}'.format(sum([count_1478(line) for line in test_data]), 26))
print('Real solution {}'.format(sum([count_1478(line) for line in common.Loader.load_lines()])))

print('PART TWO:')
print('{}, expected {}'.format(
    decode_line('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'), 5353))
for line in test_data:
    print('{}, expected {}'.format(decode_line(line), test_data[line]))
print('SUM {}, expected {}'.format(sum([decode_line(line) for line in test_data]), 61229))
print('REAL {}'.format(sum([decode_line(line) for line in common.Loader.load_lines()])))

# rules:
# 2 segments (1) c+f
# 3 segments (7) c+f == a
# 4 segments (4) c+f == b + d
# 5 segments (235) -> missing is BE or BF or CE (BE can be eliminated using #2, BF using #4)
# 6 segments (690) -> missing is D or E or C (C can be eliminated from #2, D from #4)
# 7 segments (8)
