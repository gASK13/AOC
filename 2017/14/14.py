import common


def xor_agg(data):
    x = 0
    for i in data:
        x ^= i
    return x


def knot_hash(line, debug=False):
    skip = 0
    data = [x for x in range(256)]
    total_skip = 0
    for i in range(64):
        for step in [ord(x) for x in line] + [17, 31, 73, 47, 23]:
            data = [x for x in reversed(data[:step])] + data[step:]
            skip_now = (step + skip) % len(data)
            data = data[skip_now:] + data[:skip_now]
            total_skip += skip_now
            skip += 1
            if debug:
                print(data)
    total_skip = total_skip % len(data)
    data = data[-total_skip:] + data[:-total_skip]
    return ''.join(["{0:08b}".format(xor_agg(data[i * 16:i * 16 + 16])) for i in range(16)])


def get_fragmentation(key):
    return [knot_hash('{}-{}'.format(key, i)) for i in range(128)]


def zero_regions(state, _x, _y):
    fields = [(_x, _y)]
    while len(fields) > 0:
        x, y = fields.pop()
        state[x] = state[x][:y] + '0' + state[x][y + 1:]
        for _dx, _dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= (x + _dx) < len(state) and 0 <= (y + _dy) < len(state[0]) and state[x + _dx][y + _dy] == '1':
                fields.append((x + _dx, y + _dy))


def count_regions(state):
    regions = 0
    for x in range(len(state)):
        for y in range(len(state[0])):
            if state[x][y] == '1':
                regions += 1
                zero_regions(state, x, y)
    return regions


print('Test {} (expected 8108)'.format(sum([x.count('1') for x in get_fragmentation('flqrgnkx')])))
print('Real {}'.format(sum([x.count('1') for x in get_fragmentation(common.Loader.load_lines()[0])])))

print('Test {} (expected 1242)'.format(count_regions(get_fragmentation('flqrgnkx'))))
print('Real {}'.format(count_regions(get_fragmentation(common.Loader.load_lines()[0]))))
