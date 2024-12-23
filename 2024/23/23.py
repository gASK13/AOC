import common
from colorama import Fore, Style, Back

def part_one(lines):
    return len([s for s in get_sets(lines)[0] if s[0][0] == 't' or s[1][0] == 't' or s[2][0] == 't'])

def get_sets(lines):
    connections = {}
    nodes = []
    for line in lines:
        n1, n2 = line.split('-')
        if n1 not in connections:
            connections[n1] = []
        if n2 not in connections:
            connections[n2] = []
        connections[n1].append(n2)
        connections[n2].append(n1)
        if n1 not in nodes:
            nodes.append(n1)
        if n2 not in nodes:
            nodes.append(n2)

    # now process and find triplets with "T"
    sets = set()
    for n1 in range(len(nodes)):
        for n2 in connections[nodes[n1]]:
            for n3 in connections[nodes[n1]]:
                if n3 in connections[n2] and n3 != n2:
                    sets.add(tuple(sorted([nodes[n1], n2, n3])))

    return sets, connections, nodes


def part_two(lines):
    sets, connections, nodes = get_sets(lines)

    while len(sets) > 0:
        new_sets = set()
        for s in sets:
            # try to add a new node to the set
            # if possible, move to new_sets
            for n in connections[s[0]]:
                if n not in s:
                    if all([n in connections[s2] for s2 in s]):
                        new_sets.add(tuple(sorted(list(s) + [n])))

        if len(new_sets) == 0:
            return ','.join(sorted(list(s)))
        sets = new_sets

    # we should end with
    raise Exception('No solution found - should not happen!')


assert part_one(common.Loader.load_lines('test')) == 7

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test')) == 'co,de,ka,ta'

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')

