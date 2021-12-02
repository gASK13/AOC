from common.loader import Loader

lines = Loader.load_lines()
v2 = 0
v1 = 0
h = 0
aim = 0
for line in lines:
    num = int(line.split(' ')[1])
    if line.startswith('up'):
        aim -= num
        v1 -= num
    if line.startswith('down'):
        aim += num
        v1 += num
    if line.startswith('forward'):
        h += num
        v2 += aim * num

print(h * v1)
print(h * v2)
