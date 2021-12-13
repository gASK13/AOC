def spin_lock(step, length=2017):
    buffer = [0]
    for i in range(1, length + 1):
        s = step % len(buffer)
        buffer = buffer[s:] + buffer[:s] + [i]
        if buffer[-2] == 0:
            print(buffer[-1])
    return buffer


def spin_lock_v2(step, length):
    last = 0
    pos = 0
    for i in range(1, length + 1):
        pos = (pos + 1 + step) % i
        if pos == 0:
            last = i
            print(i)
    return last


print(f'Spin lock is {spin_lock(3)[0]} (expected 638)')
print(f'Real spin lock is {spin_lock(328)[0]}')
print(f'Real ANGRY spin lock is {spin_lock_v2(328, 50000000)}')