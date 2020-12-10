def find_segments(list):
    ret = []
    len = 0
    for i in list:
        if i == 1:
            len += 1
        elif i == 3:
            if len > 1:
                ret.append(len)
            len = 0
        else:
            raise Exception('NOBODY EXPECTS THE SPANISH INQUISITION!')
    if len > 1:
        ret.append(len)
    return ret


def segment_solutions(segment):
    if segment == 2:
        return 2
    elif segment == 3:
        return 4
    elif segment == 4:
        return 7
    else:
        raise Exception('NOBODY EXPECTS THE SPANISH INQUISITION!')


adapters = []

for line in open('10.txt', 'r').readlines():
    adapters.append(int(line.strip()))

# your adapter is max + 3, source i 0
adapters.append(0)
adapters.sort()
adapters.append(adapters[-1] + 3)

# Count diffs
distr = []
for i in range(1, len(adapters)):
    diff = adapters[i] - adapters[i - 1]
    if diff > 3:
        raise Exception("OVER THREE")
    if diff <= 0:
        raise Exception("TOO LOW!")
    distr.append(diff)

print(adapters)
print(distr)


# PART TWO
print(find_segments(distr))

# if I have 3113 segment, I can remove 1 item (or keep it) -> 2 solutions
# if I have 31113 segment, I can remove 2 items (at different parts -> 4 solutions
# if I have 311113 segment, I have 7 solutions
# if I have 3111113 segment, I have 12 solutions...
# I don't need to go on, since there are no bigger segments
# multiply for real solutions :)

total = 1
for segm in find_segments(distr):
    total *= segment_solutions(segm)
print(total)

