import common

test_data = [(['0: 3', '1: 2', '4: 4', '6: 4'], 24, 10)]


def solve_layers(_lines, delay=0):
    layers = {}
    result = []
    for line in _lines:
        layers[int(line.split(':')[0])] = int(line.split(' ')[1])
    for layer in layers:
        if (layer + delay) % ((layers[layer] - 1) * 2) == 0:
            result.append(layer * layers[layer])
    return result


def find_hole(_data):
    i = 0
    while True:
        if len(solve_layers(_data, i)) == 0:
            return i
        i += 1
        if i % 10000 == 0:
            print(i)


for td in test_data:
    print('Test {} (expected {})'.format(sum(solve_layers(td[0])), td[1]))
    print('Test will find hole in {} ms (expected {})' .format(find_hole(td[0]), td[2]))

print('Real {}'.format(sum(solve_layers(common.Loader.load_lines()))))
print('Real will find hole in {} ms' .format(find_hole(common.Loader.load_lines())))


