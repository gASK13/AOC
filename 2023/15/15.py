import common
from colorama import Fore, Back, Style

test_data = {'HASH': 52,
             'rn=1': 30,
             'cm-': 253,
             'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7': 1320}

def align_mirrors(line):
    lengths = [[] for _ in range(256)]
    labels = [[] for _ in range(256)]
    for part in line.split(','):
        if '-' in part:
            label = part[:-1]
            box = hash_item(label)
            if label in labels[box]:
                idx = labels[box].index(label)
                labels[box].pop(idx)
                lengths[box].pop(idx)
        if '=' in part:
            label, focus = part.split('=')
            box = hash_item(label)
            if label not in labels[box]:
                labels[box].append(label)
                lengths[box].append(focus)
            else:
                idx = labels[box].index(label)
                lengths[box][idx] = focus
    return sum([sum([(idx+1)*(sidx+1)*(int(focus)) for sidx, focus in enumerate(box)]) for idx, box in enumerate(lengths)])




def hash_line(line):
    return sum([hash_item(part) for part in line.split(',')])

def hash_item(line):
    hsh = 0
    for c in line:
        hsh += ord(c)
        hsh *= 17
        hsh %= 256
    return hsh


for data, result in test_data.items():
    if hash_line(data) != result:
        print(f'{Fore.RED} Data not matching for {data} - {hash_line(data)}/{result}')

print(f'Part 1: {hash_line(common.Loader.load_lines()[0])}')


assert align_mirrors('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7') == 145

print(f'Part 2: {align_mirrors(common.Loader.load_lines()[0])}')