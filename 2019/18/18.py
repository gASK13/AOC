import re


def hash(_key, _keys):
    return '{}#{}'.format(_key, '$'.join(_keys))


def find_paths_from(_map, _x, _y):
    _visited = [(_x, _y)]
    # PATH = (WHERE, LEN, KEYS_NEEDED, KEYS_GOTTEN)
    # STACK = (X, Y, LEN, DOORS, KEYS)
    stack = [(_x, _y, 0, [], [])]
    paths = []
    while len(stack) > 0:
        curr = stack.pop(0)
        cx = curr[0]
        cy = curr[1]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            # for all 4 directions, see if you visited them
            # if not, put on stack
            # also if path, save!
            if (0 <= cx + dx < len(_map[0])) & (0 <= cy + dy < len(_map)) & ((cx + dx, cy + dy) not in _visited):
                _visited.append((cx + dx, cy + dy))
                chr = _map[cy + dy][cx + dx]
                if re.match('[a-z]', chr):
                    paths.append((chr, curr[2] + 1, curr[3], curr[4] + [chr]))
                    stack.append((cx + dx, cy + dy, curr[2] + 1, curr[3], curr[4] + [chr]))
                elif re.match('[A-Z]', chr):
                    stack.append((cx + dx, cy + dy, curr[2] + 1, curr[3] + [chr.lower()], curr[4]))
                elif re.match('[.@]', chr):
                    stack.append((cx + dx, cy + dy, curr[2] + 1, curr[3], curr[4]))

    return paths


map = []
for line in open('18.txt', 'r').readlines():
    map.append(line.strip())

# find path from each key to each other key
paths = {}
for (y, line) in enumerate(map):
    for (x, char) in enumerate(line):
        if re.match('[a-z@]', char):
            paths[char] = find_paths_from(map, x, y)

print(paths)

# PATH = (WHERE, LEN, KEYS_NEEDED, KEYS_GOTTEN)
# STACK = (LOCATION, STEPS, KEYS, PATH)
# now start at @ and go to each you can
# from each go to each other you can and so on, branching accordingly
stack = [('@', 0, [], ['@'])]
done = []
best = {}
while len(stack) > 0:
    stack.sort(key=lambda l: l[1])
    curr = stack.pop(0)
    #print('Stack: {}, min is {} with {} keys'.format(len(stack), curr[1], len(curr[2])))
    if len(curr[2]) == len(paths) - 1:
        print(curr)
        print('Least steps is {}'.format(curr[1]))
        break
    for path in paths[curr[0]]:
        # find all paths leading to unvisited nodes where I have keys and put on stack
        if path[0] not in curr[2]:
            if all([key in curr[2] for key in path[2]]):
                new_keys = list(set(curr[2] + path[3]))
                new_keys.sort()
                h = hash(path[0], new_keys)
                if h not in best:
                    stack.append((path[0], curr[1] + path[1], new_keys, curr[3] + [path[0]]))
                    best[h] = curr[1] + path[1]
                elif best[h] > curr[1] + path[1]:
                    stack.append((path[0], curr[1] + path[1], new_keys, curr[3] + [path[0]]))
                    best[h] = curr[1] + path[1]
