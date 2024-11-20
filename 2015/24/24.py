import common
from colorama import Fore, Back, Style

def product(array):
    result = 1
    for item in array:
        result *= item
    return result

def find_all_groups(weights):
    _groupwt = sum(weights) // 3
    assert sum(weights) == (_groupwt) * 3
    return get_sums([], weights, _groupwt)

def qe(group):
    prod = 1
    for g in group:
        prod *= g
    return prod

def get_sums(current, weights, target):
    results = []
    cs = sum(current)
    for i in range(len(weights)):
        if cs + weights[i] == target:
            results.append((current + [weights[i]], qe(current + [weights[i]])))
        elif cs + weights[i] < target:
            results.extend(get_sums(current + [weights[i]], weights[i+1:], target))
    return results

def are_exclusive(g1, g2):
    return not set(g1) & set(g2)

def part_one(weights):
    # order groups by "size" and "qe" to try to find the best quickest
    groups = find_all_groups(weights)
    best = {"qe": 1000000000, "group_size": len(weights)}
    for i in range(len(groups)):
        if len(groups[i][0]) < best["group_size"] or (len(groups[i][0]) == best["group_size"] and groups[i][1] < best["qe"]):
            if has_valid_breakdown(groups, i):
                best["qe"] = groups[i][1]
                best["group_size"] = len(groups[i][0])
                print(f"New best is {best['qe']} with {best['group_size']}")
    return best["qe"]

def has_valid_breakdown(groups, i):
    for j in range(len(groups)):
        if are_exclusive(groups[i][0], groups[j][0]):
            for k in range(j, len(groups)):
                if are_exclusive(groups[i][0] + groups[j][0], groups[k][0]):
                    return True
    return False

assert are_exclusive([1,2,3], [4,5,6])
assert not are_exclusive([1,2,3], [4,5,1])
assert part_one([1, 2, 3, 4, 5, 7, 8, 9, 10, 11]) == 99

print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines(numeric=True))}')

