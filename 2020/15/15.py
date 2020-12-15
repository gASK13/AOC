#input = [0, 3, 6]
input = [6,3,15,13,1,0]

map = {}
step = 1
while len(input) > 0:
    element = input.pop(0)
    map[element] = step
    step += 1

# Stupid solution - 30M takes a couple minutes, so I just ... wait :D
next = 0
while step <= 30000000:
    if step % 1000000 == 0:
        print('Step {}, Number {}'.format(step, next))
    if next in map:
        last = map[next]
        map[next] = step
        next = step - last
    else:
        map[next] = step
        next = 0
    step += 1