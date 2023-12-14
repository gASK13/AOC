def hash_list(_list, delimiter='#'):
    return delimiter.join([str(x) for x in _list])


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def transpose_matrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def rotate_matrix_ccw(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]


def rotate_matrix_cw(m):
    return [[m[j][i] for j in range(len(m) - 1, -1, -1)] for i in range(len(m[0]))]


# Pathfinding (see 2022/12 or 2016/13)
# map processing (see above - especially steps and navigation "outside")
