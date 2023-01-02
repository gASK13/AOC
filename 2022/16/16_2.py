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

    def open(self, minute):
        return self.rate * max(30 - minute, 0)

    def get_max(self, opened, valves, minute, curr):
        m = curr
        for v in valves:
            if v.id not in opened and v.rate > 0:
                m += v.open(minute + self.paths[v.id] + 1)
        return m


def hash(obj):
    return hash_inner(obj["pos"].id, obj["opened"])


def hash_inner(pos, opened):
    return f'{pos}##{"x".join(opened)}'


def hashes(obj):
    return [hash_inner(obj["pos"].id, o) for o in sub_lists(obj["opened"])]


def get_minute(obj):
    return obj["flow"]


def path(valves):
    v_map = {}
    for v in valves:
        v_map[v.id] = v
    for v in valves:
        v.build_paths(v_map)

    buffer = [{"pos": v_map['AA'], "minute": 1, "flow": v_map['AA'].open(0), "opened": ['AA']}]
    for path in v_map['AA'].paths:
        buffer.append({"pos": v_map[path],
                       "minute": v_map['AA'].paths[path] + 1,
                       "flow": v_map[path].open(v_map['AA'].paths[path] + 1),
                       "opened": [path]})
    seen = {}

    mflow = {"pos": v_map['AA'], "minute": 0, "flow": 0, "opened": []}
    while len(buffer) > 0:
        buffer.sort(key=get_minute)
        current = buffer.pop()
        skip = False
        for h in hashes(current):
            if h in seen and seen[h] >= current["flow"]:
                skip = True
        if skip:
            continue
        seen[hash(current)] = current["flow"]
        if current["minute"] >= 30:
            continue
        if current["flow"] >= mflow["flow"]:
            mflow = current
        for path in current["pos"].paths:
            if path not in current["opened"]:
                if v_map[path].get_max(current["opened"] + [path], valves,
                                       current["minute"] + current["pos"].paths[path] + 1,
                                       current["flow"] + v_map[path].open(
                                               current["minute"] + current["pos"].paths[path] + 1)) >= mflow[
                    "flow"]:
                    buffer.append({"pos": v_map[path],
                                   "minute": current["minute"] + 1 + current["pos"].paths[path],
                                   "flow": current["flow"] + v_map[path].open(
                                       current["minute"] + current["pos"].paths[path] + 1),
                                   "opened": sorted(current["opened"] + [path])})
    print(mflow)
    return mflow["flow"]


assert path(common.Loader.transform_lines(Valve, 'test')) == 1651
print(f'Flow is {path(common.Loader.transform_lines(Valve))}') #1796

#assert path(common.Loader.transform_lines(Valve, 'test')) == 1707
#print(f'Elephant flow is {path(common.Loader.transform_lines(Valve))}')
