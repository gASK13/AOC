import common
from colorama import Fore, Back, Style


def parse_input(lines):
    _map = {}
    for line in lines:
        origin, targets = line.split(': ')
        for target in targets.split(' '):
            _map[origin] = _map.get(origin, set())
            _map[origin].add(target)
            _map[target] = _map.get(target, set())
            _map[target].add(origin)
    return _map


def get_edges(_map):
    edges = []
    for node in _map:
        for edge in _map[node]:
            if (node, edge) not in edges and (edge, node) not in edges:
                edges.append((node, edge))
    return edges


def compact(_map, _exceptions):
    nodes = [next(iter(_map.keys()))]
    buffer = [(nodes[0], x) for x in _map[nodes[0]]]

    while len(buffer) > 0:
        origin, target = buffer.pop()
        if (origin, target) in _exceptions or (target, origin) in _exceptions:
            continue
        if target in nodes:
            continue
        nodes.append(target)
        buffer += [(target, x) for x in _map[target] if x not in nodes]

    if len(nodes) != len(_map) and len(nodes) > 1 and len(_map) - len(nodes) > 1:
        print(f'With {_exceptions} found {len(nodes)} nodes out of {len(_map)}')
        return len(nodes) * (len(_map) - len(nodes))

    return None


def part_1_new(lines):
    _map = parse_input(lines)

    nodes = [n for n in _map.keys()]

    # split in two halves - semirandom > based on number of neighbors in current G2
    group_2 = set([n for n in nodes[1:]])
    group_1 = set([nodes[0]])

    while len(group_2) > len(group_1):
        # find node in g2 with most connections to g1
        best_node = None
        best_score = 0
        for node in group_2:
            score = sum([1 for e in _map[node] if e in group_1])
            if score > best_score:
                best_score = score
                best_node = node
        group_2.remove(best_node)
        group_1.add(best_node)

    # optimization - so we don't compute score for variants which have no new edges between groups
    # so we have sets of only "viable" candidates
    candidates_1 = set()
    candidates_2 = set()
    for node in group_1:
        for edge in _map[node]:
            if edge in group_2:
                candidates_1.add(node)
                candidates_2.add(edge)


    # compute "division size"
    # if > 3, then try to rebalance nodes back and forth
    while get_partition_size(_map, group_1, group_2) > 3:
        # find node with the best "new score", weighted by size of the other group
        # this is to avoid "bleeding" the group dry (since it will eat as many nodes as possible)
        best_node = None
        best_score = 999999
        best_node, best_score = find_best_node(_map, best_node, best_score, candidates_1, group_1, group_2)
        best_node, best_score = find_best_node(_map, best_node, best_score, candidates_2, group_2, group_1)

        # move the best node it to the other group
        if best_node in group_1:
            group_1.remove(best_node)
            group_2.add(best_node)
        else:
            group_2.remove(best_node)
            group_1.add(best_node)

        # recount candidates (quick and dirty "just remake it" approach)
        candidates_1 = set()
        candidates_2 = set()
        for node in group_1:
            for edge in _map[node]:
                if edge in group_2:
                    candidates_1.add(node)
                    candidates_2.add(edge)

    return len(group_1) * len(group_2)


def find_best_node(_map, best_node, best_score, candidates_1, group_1, group_2):
    for node in candidates_1:
        group_1.remove(node)
        group_2.add(node)
        ps = get_partition_size(_map, group_1, group_2) * len(group_2)
        if ps < best_score:
            best_score = ps
            best_node = node
        group_1.add(node)
        group_2.remove(node)
    return best_node, best_score


def get_partition_size(_map, g1, g2):
    ps = 0
    for n in g1:
        for e in _map[n]:
            if e in g2:
                ps += 1
    return ps


assert part_1_new(common.Loader.load_lines('test')) == 54
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{part_1_new(common.Loader.load_lines())}')
