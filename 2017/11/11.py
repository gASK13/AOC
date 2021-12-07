import common
from collections import Counter

test_data = {
    'ne,ne,ne': 3,
    'ne,ne,sw,sw': 0,
    'ne,ne,s,s': 2,
    'se,sw,se,sw,sw': 3,
    'n,n,n,ne,ne,ne': 6,
    's,s,sw,sw': 4,
    's,s,n,sw,sw,s,nw,se': 4,
    'nw,nw,nw': 3,
    'se,s,n': 1,
    'nw,n,n': 3,
    'n,ne,nw,nw': 3,
    'n,ne,nw': 2
}


def get_hex_distance(data):
    c = Counter(data)
    s = c['s'] - c['n']
    ne = c['ne'] - c['sw']
    nw = c['nw'] - c['se']
    nw -= s
    ne -= s
    if ne > 0 and nw > 0:
        return max(ne, nw)
    if ne < 0 and nw < 0:
        return -min(ne, nw)
    else:
        return abs(nw+ne)


for t in test_data:
    print('{} -> {} steps ({})'.format(t, get_hex_distance(t.split(',')), test_data[t]))

data = common.Loader.load_matrix(delimiter=',')[0]
print(get_hex_distance(data))
print(max([get_hex_distance(data[:x]) for x in range(len(data))]))
