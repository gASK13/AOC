# oh boy, I took the math route to part 1 and part 2 became ... harder ... oof


def compute_neighbors(_matrix, _coords):
    sum_neighbors = 0
    for i in range(_coords[0] - 1, _coords[0] + 2):
        for j in range(_coords[1] - 1, _coords[1] + 2):
            if (i, j) in _matrix:
                sum_neighbors += _matrix[(i, j)]
    return sum_neighbors


matrix = {(0, 0): 1}

coords = (0, 1)
num = 1
level = 1
state = [(-1, 0), level]

input = 289326

while True:
    num = compute_neighbors(matrix, coords)
    print("{} == {}".format(coords, num))
    if num > input:
        break
    matrix[coords] = num
    coords = (coords[0] + state[0][0], coords[1] + state[0][1])
    state[1] -= 1
    if state[1] == 0:
        # turn around
        state[0] = (-state[0][1], state[0][0])
        if state[0][0] == 0:
            level += 1
        state[1] = level