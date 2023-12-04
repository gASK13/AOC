import common

test_routes = ['London to Dublin = 464', 'London to Belfast = 518', 'Dublin to Belfast = 141']


def generate_map(routes):
    _map = {}
    for route in routes:
        distance = int(route.split(' = ')[1])
        cities = route.split(' = ')[0].split(' to ')
        if cities[0] not in _map:
            _map[cities[0]] = {}
        if cities[1] not in _map:
            _map[cities[1]] = {}
        _map[cities[0]][cities[1]] = distance
        _map[cities[1]][cities[0]] = distance
    return _map


def compute_hash(where, visited):
    return f'{where}@@@{"#".join(sorted(visited))}'

def find_shortes_route(_map):
    paths = []
    final = []
    hashes = {}
    for city in _map:
        paths.append((city, 0, [city]))
    while len(paths) > 0:
        (where, long, visited) = paths.pop(0)
        if compute_hash(where, visited) in hashes and hashes[compute_hash(where, visited)] < long:
            continue
        hashes[compute_hash(where, visited)] = long
        print(f'Visiting {where} with {long} and {visited} ({len(paths)} paths left)')
        for city in _map[where]:
            if city not in visited:
                paths.append((city, long + _map[where][city], visited + [city]))
        if len(visited) == len(_map):
            final.append((long, visited))
    print(final)
    return min([long for (long, visited) in final])


def find_longest_route(_map):
    paths = []
    final = []
    hashes = {}
    for city in _map:
        paths.append((city, 0, [city]))
    while len(paths) > 0:
        (where, long, visited) = paths.pop(0)
        if compute_hash(where, visited) in hashes and hashes[compute_hash(where, visited)] >= long:
            continue
        hashes[compute_hash(where, visited)] = long
        print(f'Visiting {where} with {long} and {visited} ({len(paths)} paths left)')
        for city in _map[where]:
            if city not in visited:
                paths.append((city, long + _map[where][city], visited + [city]))
        if len(visited) == len(_map):
            final.append((long, visited))
    print(final)
    return max([long for (long, visited) in final])


assert find_shortes_route(generate_map(test_routes)) == 605

assert find_longest_route(generate_map(test_routes)) == 982

print(f'Shortest route is {find_shortes_route(generate_map(common.Loader.load_lines()))}')
print(f'Longest route is {find_longest_route(generate_map(common.Loader.load_lines()))}')
