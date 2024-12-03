from array import array

import common
import re

test_data = {"mul(44,46)": 2024,
             "mul(123,4)":123*4,
             "mul(4*" : 0,
             "mul(6,9!" : 0,
             "?(12,34)" : 0,
             "mul ( 2 , 4 )": 0,
             "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))" : 161}

def part_one(lines):
    if isinstance(lines, list):
        lines = ''.join(lines)
    sum = 0
    for part in re.findall('mul\([0-9]+,[0-9]+\)', lines.strip()):
        nums = part[4:-1].split(',')
        sum += int(nums[0]) * int(nums[1])
    return sum

def part_two(lines):
    if isinstance(lines, list):
        lines = ''.join(lines)
    return part_one(re.sub("don't\(\).*?(do\(\)|$)", "", lines))

for key in test_data:
    assert part_one(key) == test_data[key]

print(f'Part one: {part_one(common.Loader.load_lines())}')

assert part_two("xmul(2,4)&mul[3,7]!^do()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))") == 48+25+88
assert part_two("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))") == 48
assert part_two("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))") == 96
assert part_two("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)un?mul(8,5))") == 8
assert part_two(["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)un?mul(8,5))",
                "ihrgehigaoirgmul(2,5)nebomul(10,10)nebo_do()_mul(9,5)"]) == 8+45

print(f'Part two: {part_two(common.Loader.load_lines())}')

