import common
from itertools import combinations


def sub_lists(l):
    comb = []
    for i in range(len(l) + 1):
        comb += [list(j) for j in combinations(l, i)]
    return comb

class Valve:
    def __init__(self, line):
        stuff = line.split(' ')
        self.id = stuff[1]
        self.rate = int(stuff[4].split('=')[1][:-1])
        self.other_id = [x[:2] for x in stuff[9:]]
        self.others = {}
        self.paths = {}

    def open(self, minute):
        return self.rate * max(30 - minute, 0)

    def build_paths(self, valves):
        buffer = [(self, 0)]
        while len(buffer) > 0:
            v, pth = buffer.pop(0)
            for next_v in v.other_id:
                if next_v not in self.paths:
                    self.paths[next_v] = pth + 1
                    buffer.append((valves[next_v], pth + 1))
        to_del = set([self.id])
        for p in self.paths:
            if valves[p].rate == 0:
                to_del.add(p)
        for d in to_del:
            del self.paths[d]

    def get_max(self, opened, valves, minute, curr):
        m = curr
        for v in valves:
            if v.id not in opened and v.rate > 0:
                m += v.open(minute + (self.paths[v.id] if v.id != self.id else 0) + 1)
        return m


def has_cycle(path):
    for i in range(2, 5):
        if len(path) >= 2*i and path[-i:] == path[-i*2:-i]:
            return True
    return False


def hash(vid, opened):
    return f'{vid}##{"x".join(sorted(opened))}'


def hashes(vid, opened):
    return [hash(vid, o) for o in sub_lists(opened)]


def path(valves):
    v_map = {}
    for v in valves:
        v_map[v.id] = v
    for v in valves:
        v.build_paths(v_map)

    seen = {}
    mflow = (None, None, None, 0, None)
    buffer = [(v_map['AA'], ['AA'], 0, 0, [])]
    while len(buffer) > 0:
        (v, path, minute, flow, opened) = buffer.pop(0)
        skip = False
        for h in hashes(v.id, opened):
            if h in seen and seen[h] >= flow:
                skip = True
        if skip:
            continue
        seen[hash(v.id, opened)] = flow
        if mflow[3] < flow:
            mflow = (v, path, minute, flow, opened)
        if minute == 30:
            continue
        if v.id not in opened:
            buffer.append((v, path, minute+1, flow + v.open(minute + 1), opened + [v.id]))
        for id in v.other_id:
            if v_map[id].get_max(opened, valves, minute+1, flow) > mflow[3]:
                buffer.append((v_map[id], path + [id], minute+1, flow, opened))
    print(mflow)
    return mflow[3]


assert path(common.Loader.transform_lines(Valve, 'test')) == 1651
print(f'Flow is {path(common.Loader.transform_lines(Valve))}')
