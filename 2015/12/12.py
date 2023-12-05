import common
import json


def sum_string(string, red_filter=False):
    # decode json from string
    data = json.loads(string)
    return sum_numbers(data, red_filter)


def sum_numbers(data, red_filter=False):
    if isinstance(data, int):
        return data
    elif isinstance(data, list):
        return sum([sum_numbers(item, red_filter) for item in data])
    elif isinstance(data, dict):
        if 'red' in data.values() and red_filter:
            return 0
        return sum([sum_numbers(item, red_filter) for item in data.values()])
    return 0


assert sum_string("[1, 2, 3]") == 6
assert sum_string('{"a": 2, "b": 4}') == 6
assert sum_string("[[3]]") == 3
assert sum_string('{"a": {"b": 4}, "c": -1}') == 3
assert sum_string('{"a": [-1, 1]}') == 0
assert sum_string('[-1,{"a":1}]') == 0
assert sum_string('[]') == 0
assert sum_string('{}') == 0
assert sum_string('[1,{"c":"red","b":2},3]', True) == 4
assert sum_string('[1,2,3]', True) == 6
assert sum_string('[1,"red",5]', True) == 6

print(f'Part 1: {sum_string(common.Loader.load_lines()[0])}')
print(f'Part 2: {sum_string(common.Loader.load_lines()[0], True)}')
