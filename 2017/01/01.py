def get_digits(list, step = None):
    sum = 0
    if step is None:
        step = int(len(list) / 2)
    for i in range(0, len(list)):
        if list[i-step] == list[i]:
            sum += int(list[i])
    return sum


print(get_digits('1122', 1))
print(get_digits('1111', 1))
print(get_digits('1234', 1))
print(get_digits('91212129', 1))
print(get_digits(open('input.txt', 'r').readline().strip(), 1))

print(get_digits('1212'))
print(get_digits('1221'))
print(get_digits('123425'))
print(get_digits('123123'))
print(get_digits('12131415'))
print(get_digits(open('input.txt', 'r').readline().strip()))