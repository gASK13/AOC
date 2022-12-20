import common


def decrypt(values, n=1, key=1):
    items = [i for i in range(len(values))]
    values = [v * key for v in values]
    for i in range(n):
        for i in range(len(values)):
            idx = items.index(i)
            move = values[idx]
            newpos = (idx + move) % (len(values) - 1)
            if newpos == 0:
                newpos += len(values) - 1
            if newpos < idx:
                values = values[:newpos] + [move] + values[newpos:idx] + values[idx+1:]
                items = items[:newpos] + [i] + items[newpos:idx] + items[idx + 1:]
            if newpos > idx:
                values = values[:idx] + values[idx+1:newpos+1] + [move] + values[newpos+1:]
                items = items[:idx] + items[idx+1:newpos+1] + [i] + items[newpos+1:]
    return values


def compute_sum(values):
    offset = values.index(0)
    return values[(offset + 1000) % len(values)] + values[(offset + 2000) % len(values)] + values[(offset + 3000) % len(values)]


assert decrypt([1, 2, -3, 3, -2, 0, 4]) == [1, 2, -3, 4, 0, 3, -2]
assert compute_sum(decrypt([1, 2, -3, 3, -2, 0, 4])) == 3
print(f'1st part: {compute_sum(decrypt(common.Loader.load_lines(numeric=True)))}')


assert decrypt([1, 2, -3, 3, -2, 0, 4], n=10, key=811589153) == [-2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153, 0]
assert compute_sum(decrypt([1, 2, -3, 3, -2, 0, 4], n=10, key=811589153)) == 1623178306
print(f'2nd part: {compute_sum(decrypt(common.Loader.load_lines(numeric=True), n=10, key=811589153))}')