import common


def area(edges):
    sides = [edges[i] * edges[i - 1] for i in range(len(edges))]
    sides.sort()
    return sum(sides) * 2 + sides[0]


def ribbon(edges):
    sides = [edges[i] + edges[i - 1] for i in range(len(edges))]
    sides.sort()
    return sides[0] * 2 + (edges[0] * edges[1] * edges[2])


test_data = {(2, 3, 4): (58, 34), (1, 1, 10): (43, 14)}
for t in test_data:
    assert area(t) == test_data[t][0]
    assert ribbon(t) == test_data[t][1]

print(f'Paper needed is {sum([area(gift) for gift in common.Loader.load_matrix(delimiter="x", numeric=True)])} sqfeet.')
print(f'Ribbon needed is {sum([ribbon(gift) for gift in common.Loader.load_matrix(delimiter="x", numeric=True)])} feet.')
