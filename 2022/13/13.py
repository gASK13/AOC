import common
import json
import functools


def convert_to_list(_list):
    if not isinstance(_list, list):
        if isinstance(_list, int):
            return [_list]
        else:
            return json.loads(_list)
    return list(_list)


def compare_lists(list1, list2):
    list1 = convert_to_list(list1)
    list2 = convert_to_list(list2)
    while len(list1) > 0:
        if len(list2) == 0:
            return -1  # ran out of items (right side)
        item1 = list1.pop(0)
        item2 = list2.pop(0)
        if isinstance(item1, list) or isinstance(item2, list):
            ret = compare_lists(item1, item2)
            if ret != 0:
                return ret
        else:
            if item1 < item2:
                return 1
            if item1 > item2:
                return -1
            # same? continue
    if len(list2) > 0:
        return 1
    return 0


def process_input_first(input):
    return sum([i + 1 for i in range((len(input) + 1) // 3) if compare_lists(input[i * 3], input[i * 3 + 1]) == 1])


def process_input_second(input):
    packets = [line for line in input if line != ''] + [[[2]], [[6]]]
    packets = sorted(packets, reverse=True, key=functools.cmp_to_key(compare_lists))
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


assert compare_lists([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) == 1
assert compare_lists('[1,1,3,1,1]', '[1,1,5,1,1]') == 1
assert compare_lists([[1], [2, 3, 4]], [[1], 4]) == 1
assert compare_lists('[[1],[2,3,4]]', '[[1],4]') == 1
assert compare_lists('[9]', '[[8,7,6]]') == -1
assert compare_lists([[4, 4], 4, 4], [[4, 4], 4, 4, 4]) == 1
assert compare_lists([7, 7, 7, 7], [7, 7, 7]) == -1
assert compare_lists([], [3]) == 1
assert compare_lists([[[]]], [[]]) == -1
assert compare_lists([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]) == -1

assert process_input_first(common.Loader.load_lines('test')) == 13
print(f'Sum of pairs is {process_input_first(common.Loader.load_lines())}')

assert process_input_second(common.Loader.load_lines('test')) == 140
print(f'Sum of sorted pairs is {process_input_second(common.Loader.load_lines())}')
