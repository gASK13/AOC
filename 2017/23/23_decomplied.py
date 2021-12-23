def is_prime(n):
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))

def run(debug):
    h = 0
    start = 93
    end = 93
    if not debug:
        start = 109300
        end = 126300
    for b in range(start, end+1, 17):
        if not is_prime(b):
            h += 1
    return h

print(run(True))
print(run(False))

# 2185 is not right???
# (93, 93, 93, 93, 0, 0, 1)