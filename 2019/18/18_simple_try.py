import re


def hash(_keys):
    _keys.sort()
    return '@' + ''.join(_keys)


def find_paths_from(_map, _x, _y):
    _visited = [(_x, _y)]
    # PATH = (WHERE, LEN, KEYS_NEEDED, KEYS_GOTTEN)
    # STACK = (X, Y, LEN, DOORS, KEYS)
    stack = [(_x, _y, 0, [], [])]
    paths = []
    while len(stack) > 0:
        curr = stack.pop()
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
pos = None
key_count = 0
for (row, line) in enumerate(open('18.txt', 'r').readlines()):
    for (x, char) in enumerate(line):
        if char == '@':
            pos = (x, row)
        elif re.match('[a-z]', char):
            key_count += 1
    map.append(line.strip())

# STACK - position, steps, keys, hash
# MAP - dict of keys / min steps
step_map =[[{} for char in line] for line in map]
step_map[pos[1]][pos[0]]['@'] = True
stack = [(pos[0], pos[1], 0, [], '@')]
iters = 0
while len(stack) > 0:
    iters += 1
    stack.sort(key=lambda sk: sk[2])
    curr = stack.pop(0)
    cx = curr[0]
    cy = curr[1]
    if iters % 10000 == 0:
        print('{} # Stack: {}, Curr: {}'.format(iters, len(stack), curr))
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        # for all 4 directions, see if you visited them
        # if not, put on stack
        # also if path, save!
        if (0 <= cx + dx < len(map[0])) & (0 <= cy + dy < len(map)) & (curr[4] not in step_map[cy + dy][cx + dx]):
            step_map[cy + dy][cx + dx][curr[4]] = True
            cell = map[cy + dy][cx + dx]
            if re.match('[a-z]', cell):
                if cell in curr[3]:
                    stack.append((cx + dx, cy + dy, curr[2] + 1, curr[3], curr[4]))
                else:
                    if len(curr[3]) + 1 == key_count:
                        print(curr[2] + 1)
                        exit()
                    stack.append((cx + dx, cy + dy, curr[2] + 1, curr[3] + [cell], hash(curr[3] + [cell])))
            elif re.match('[A-Z]', cell):
                if cell.lower() in curr[3]:
                    stack.append((cx + dx, cy + dy, curr[2] + 1, curr[3], curr[4]))
            elif re.match('[.@]', cell):
                stack.append((cx + dx, cy + dy, curr[2] + 1, curr[3], curr[4]))

