# I never really ran those, after I "decompiled" the code, it became obvious
# this is just "digit check" in a very roundabout way

def parse_input(input):
    return [input % pow(10, i) // pow(10, i-1) for i in range(14,0, -1)]


def validate(input):
    w = parse_input(input)
    if w[2] + 5 != w[3]:
        return False
    if w[4] - 3 != w[5]:
        return False
    if w[6] + 7 != w[7]:
        return False
    if w[9] - 1 != w[10]:
        return False
    if w[8] + 3 != w[11]:
        return False
    if w[1] + 6 != w[12]:
        return False
    if w[0] != w[13]:
        return False
    return len(z) == 0


print(93499629698999)  # Part ONE (manual labor)
print(11164118121471)  # Part TWO (manual labor)
