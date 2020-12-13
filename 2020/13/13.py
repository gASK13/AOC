# This function computes GCD
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


# This function computes LCM
def lcm(x, y):
    return (x*y)//gcd(x,y)


f = open('13.txt', 'r')
arrival = int(f.readline().strip())
busses = []
best_bus = (99999, 0)
diff = 0
for bus in f.readline().strip().split(','):
    if bus != 'x':
        busd = int(bus)
        busses.append((busd, diff, 0))
        if (busd - (arrival % busd)) % busd < best_bus[0]:
            best_bus = ((busd - (arrival % busd)) % busd, busd)
    diff += 1

#SETUP
print(busses)

#PART ONE
print(best_bus)
print('RESULT PART ONE {}'.format(best_bus[0] * best_bus[1]))

#PART TWO
last_num = busses.pop(0)
while len(busses) > 0:
    next_bus = busses.pop(0)
    i = 1
    while (i * last_num[0] + last_num[2] + next_bus[1]) % next_bus[0] != 0:
        i += 1
    last_num = (lcm(last_num[0], next_bus[0]), 0, i * last_num[0] + last_num[2])
    print(last_num)

print('RESULT, PART TWO {}'.format(last_num[2]))