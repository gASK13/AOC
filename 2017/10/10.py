import common

test_data = {
    '': 'a2582a3a0e66e6e86e3812dcb672a272',
    'AoC 2017': '33efeb34ea91902bb2f59c9920caa6cd',
    '1,2,3': '3efbe78a8d82f29979031a4aa0b16a9d',
    '1,2,4': '63960835bcdc130f0b66d7ff4f6a5a8e'
}


def elf_hash(data, steps, debug=False):
    skip = 0
    total_skip = 0
    for step in steps:
        data = [x for x in reversed(data[:step])] + data[step:]
        skip_now = (step + skip) % len(data)
        data = data[skip_now:] + data[:skip_now]
        total_skip += skip_now
        skip += 1
        if debug:
            print(data)
    total_skip = total_skip % len(data)
    data = data[-total_skip:] + data[:-total_skip]
    if debug:
        print(data)
    return data


def xor_agg(data):
    x = 0
    for i in data:
        x ^= i
    return x


def knot_hash(data, line, debug=False):
    skip = 0
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
    return ''.join(["{0:02x}".format(xor_agg(data[i * 16:i * 16 + 16])) for i in range(16)])


test_list = [3, 4, 1, 5]
test_result = elf_hash([x for x in range(5)], test_list)
print('Test result is {}'.format(test_result[0] * test_result[1]))

result = elf_hash([x for x in range(256)], common.Loader.load_matrix(delimiter=',', numeric=True)[0])
print('Result is {}'.format(result[0] * result[1]))

for td in test_data:
    print('Knot hash for {} result is:\n{}\n{}'.format(td, knot_hash([x for x in range(256)], td), test_data[td]))
print('Knot hash result is {}'.format(knot_hash([x for x in range(256)], common.Loader.load_lines()[0])))
