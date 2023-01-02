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
        return self.rate * max(26 - minute, 0)

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

    def get_max(self, other, opened, valves, minute, curr):
        m = curr
        for v in valves:
            if v.id not in opened and v.rate > 0:
                m += v.open(minute + min(self.paths[v.id] if v.id != self.id else 0, other.paths[v.id] if v.id != other.id else 0) + 1)
        return m


def has_cycle(path):
    for i in range(2, 5):
        if len(path) >= 2*i and path[-i:] == path[-i*2:-i]:
            return True
    return False


def hash(vid, opened):
    return f'{vid}##{"x".join(sorted(opened))}'


def hashes(vid, opened):
    #return hash(vid, opened)
    return [hash(vid, o) for o in sub_lists(opened)]


def path(valves):
    v_map = {}
    pvalves = [v for v in valves if v.rate > 0]
    for v in valves:
        v_map[v.id] = v
    for v in valves:
        v.build_paths(v_map)

    seen = {}
    mflow = (None, None, 0, None)
    buffer = [(['AA', 'AA'], 0, 0, [])]
    i = 0
    while len(buffer) > 0:
        buffer.sort(key=lambda a: a[2])
        i += 1
        if i % 10000 == 0:
            print(f'{len(buffer)} remaining (CURR MAX {mflow[2]})')
            print(buffer[-1])
        (vs, minute, flow, opened) = buffer.pop()
        skip = False
        for h in hashes(vs, opened):
            if h in seen and minute in seen[h] and seen[h][minute] >= flow:
                skip = True
        if skip:
            continue
        seen[hash(vs, opened)] = {}
        for m in range(minute, 27):
            seen[hash(vs, opened)][m] = flow
        if mflow[2] < flow:
            mflow = (vs, minute, flow, opened)
        if minute == 26:
            continue
        if len(opened) == len(pvalves):
            continue
        if vs[0] not in opened and v_map[vs[0]].rate > 0:
            if vs[1] not in opened and v_map[vs[1]].rate > 0 and vs[0] != vs[1]:
                buffer.append(
                    (sorted([vs[0], vs[1]]), minute + 1, flow + v_map[vs[0]].open(minute + 1) + v_map[vs[1]].open(minute + 1), sorted(opened + [vs[0], vs[1]])))
            for id in v_map[vs[1]].other_id:
                buffer.append(
                    (sorted([vs[0], id]), minute + 1, flow + v_map[vs[0]].open(minute + 1), sorted(opened + [vs[0]])))
        if vs[1] not in opened and v_map[vs[1]].rate > 0:
            for id in v_map[vs[0]].other_id:
                buffer.append(
                    (sorted([vs[1], id]), minute + 1, flow + v_map[vs[1]].open(minute + 1), sorted(opened + [vs[1]])))
        for nvid in v_map[vs[0]].other_id:
            for neid in v_map[vs[1]].other_id:
                if v_map[neid].get_max(v_map[nvid], opened, valves, minute + 1, flow) >= mflow[2]:
                    buffer.append((sorted([nvid, neid]), minute + 1, flow, opened))
    print(mflow)
    return mflow[2]


assert path(common.Loader.transform_lines(Valve, 'test')) == 1707
print(f'Flow is {path(common.Loader.transform_lines(Valve))}')
