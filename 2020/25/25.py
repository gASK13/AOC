q = 20201227


def mod_by_seven(_x):
    while _x % 7 > 0:
        _x += q
    return int(_x / 7)


def get_loop_size(_x):
    loop = 0
    while _x > 1:
        _x = mod_by_seven(_x)
        loop += 1
    return loop


# a = 7^x
# b = 7^y
# ret = 7^(x*y)
a = 12578151
b = 5051300
x = get_loop_size(a)
print(pow(b, x) % q)


