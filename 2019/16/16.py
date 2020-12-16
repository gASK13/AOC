import numpy as np

def step(_input):
    next = []
    for x in range(0, len(_input)):
        # 0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1
        # 0, 1, 0, -1
        arr = np.array([(i // (x + 1)) % 2 * (2 - (i // (x + 1)) % 4) for i in range(1, len(input_np) + 1)])
        next.append(abs((arr * _input).sum()) % 10)
    return np.array(next)


def format(_offset, _input):
    return ''.join([str(digit) for digit in _input[_offset:_offset+8]])


file_name = '16.txt'
input_signal = open(file_name, 'r').readline().strip()
offset = int(input_signal[0:7])

# PART ONE, LEFT OUT
#input_np = np.array([int(ch) for ch in input_signal])
#for i in range(0, 100):
    #input_np = step(input_np)

#print(format(0, input_np))

input_np = np.array(np.array([[int(ch) for ch in input_signal] for i in range(0, 10000)]).flat)[offset:]
print(offset)
print(len(input_np))

# I don't know if LUCKY or WHAt, but offset is behind half
# that means no holes, no -1 -> Nth element is sum of all elements behind it, so I can do formulas
formulas = [1 for item in input_np]
for i in range(0, 99): # not 100, but 99 - first phase is 1's
    for x in range(1, len(formulas)):
        formulas[x] += formulas[x-1]
        formulas[x] %= 10

# COmPUTE ALL 8 digits
result = ''
for x in range(0, 8):
    if x == 0:
        forms = formulas
    else:
        forms = formulas[:-x]
    res = (input_np[x:] * np.array(forms)).sum()
    result += str(res % 10)

print(result)





