import common

def solve_first(lines):
    lists = common.transpose_matrix(lines)
    lists[0].sort()
    lists[1].sort()
    sum = 0
    for i in range(len(lists[0])):
        sum += abs(lists[0][i] - lists[1][i])
    return sum

def solve_second(lines):
    lists = common.transpose_matrix(lines)
    occurences = {}
    for i in range(len(lists[1])):
        if lists[1][i] not in occurences:
            occurences[lists[1][i]] = 0
        occurences[lists[1][i]] += 1
    return sum([occurences[x]*x if x in occurences else 0 for x in lists[0]])

delimiter = '\\s+'
assert solve_first(common.Loader.load_matrix('test', numeric=True, delimiter=delimiter)) == 11
print(f"Part 1: {solve_first(common.Loader.load_matrix(numeric=True, delimiter=delimiter))}")

assert solve_second(common.Loader.load_matrix('test', numeric=True, delimiter=delimiter)) == 31
print(f"Part 2: {solve_second(common.Loader.load_matrix(numeric=True, delimiter=delimiter))}")