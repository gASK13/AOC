import common


def look_and_say(number):
    result = ""
    prev_char = None
    for char in number:
        if prev_char is None:
            prev_char = char
            count = 1
        elif prev_char == char:
            count += 1
        else:
            result += str(count) + prev_char
            prev_char = char
            count = 1
    result += str(count) + prev_char
    return result


def iterate(method, number, count = 40):
    for _ in range(count):
        number = method(number)
    return number


assert look_and_say("1") == "11"
assert look_and_say("11") == "21"
assert look_and_say("21") == "1211"
assert look_and_say("1211") == "111221"
assert look_and_say("111221") == "312211"
assert look_and_say("312211") == "13112221"

print(f'Part 1: {len(iterate(look_and_say, common.Loader.load_lines()[0]))}')
print(f'Part 2: {len(iterate(look_and_say, common.Loader.load_lines()[0], 50))}')