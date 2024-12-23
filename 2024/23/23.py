import common
from colorama import Fore, Style, Back

def part_one(lines):
    return len([s for s in get_sets(lines) if s[0][0] == 't' or s[1][0] == 't' or s[2][0] == 't'])

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
        for n2 in range(n1+1, len(nodes)):
            for n3 in range(n2+1, len(nodes)):
                if nodes[n2] in connections[nodes[n1]] and nodes[n3] in connections[nodes[n1]] and nodes[n2] in connections[nodes[n3]]:
                    sets.add((nodes[n1],nodes[n2], nodes[n3]))

    return sets


def part_two(lines):
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
        for n2 in range(n1 + 1, len(nodes)):
            for n3 in range(n2 + 1, len(nodes)):
                if nodes[n2] in connections[nodes[n1]] and nodes[n3] in connections[nodes[n1]] and nodes[n2] in \
                        connections[nodes[n3]]:
                    sets.add((nodes[n1], nodes[n2], nodes[n3]))

    return sets


assert part_one(common.Loader.load_lines('test')) == 7

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines())}{Style.RESET_ALL}')

assert part_two(common.Loader.load_lines('test')) == 'co,de,ka,ta'

print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines())}{Style.RESET_ALL}')

