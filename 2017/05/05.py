from common.loader import Loader


def run_offset_machine(_data, strange=False):
    position = 0
    steps = 0
    while position in range(0, len(_data)):
        offset = _data[position]
        if strange & (_data[position] >= 3):
            _data[position] -= 1
        else:
            _data[position] += 1
        position += offset
        steps += 1

    return steps


print(run_offset_machine([0, 3, 0, 1, -3]))
print(run_offset_machine(Loader.load_lines(numeric=True)))

print(run_offset_machine([0, 3, 0, 1, -3], True))
print(run_offset_machine(Loader.load_lines(numeric=True), True))

