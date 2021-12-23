import common


def build_bridges(file=None):
    components = [[int(n) for n in c.split('/')] for c in common.Loader.load_lines(file)]

    bridges = [([n for n in b if n != 0][0], [b], [x for x in components if b != x]) for b in components if 0 in b]
    finished = []

    while len(bridges) > 0:
        end, bridge, components = bridges.pop()
        extended = False
        for c in components:
            if end in c:
                if len([_ for _ in c if _ != end]) == 0:
                    xe = end
                else:
                    xe = [_ for _ in c if _ != end][0]
                xc = [_ for _ in components if _ != c]
                xb = [_ for _ in bridge] + [c]
                bridges.append((xe, xb, xc))
                extended = True
        finished.append(bridge)
    return finished


def get_strongest_bridge(bridges):
    return max([sum([sum(c) for c in b]) for b in bridges])


def filter_longest_bridges(bridges):
    longest = max([len(b) for b in bridges])
    return [b for b in bridges if len(b) == longest]


assert get_strongest_bridge(build_bridges('test.txt')) == 31
print(get_strongest_bridge(build_bridges()))

assert get_strongest_bridge(filter_longest_bridges(build_bridges('test.txt'))) == 19
print(get_strongest_bridge(filter_longest_bridges(build_bridges())))