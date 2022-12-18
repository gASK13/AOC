import common


def count_sides(cubes):
    sides = [[-1, 0, 0], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, -1], [0, 0, 1]]
    side_count = 0
    for cube in cubes:
        for side in sides:
            if [cube[0] + side[0], cube[1] + side[1], cube[2] + side[2]] not in cubes:
                side_count += 1
    return side_count

def count_surface(cubes):
    sides = [[-1, 0, 0], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, -1], [0, 0, 1]]
    start_x = sorted([x for x, y, z in cubes])[-1] + 1
    start_y = sorted([y for x, y, z in cubes])[-1] + 1
    start_z = sorted([z for x, y, z in cubes])[-1] + 1
    min_x = sorted([x for x, y, z in cubes])[0] - 1
    min_y = sorted([y for x, y, z in cubes])[0] - 1
    min_z = sorted([z for x, y, z in cubes])[0] - 1
    visited = [[start_x, start_y, start_z]]
    buffer = [[start_x, start_y, start_z]]
    side_count = 0
    while len(buffer) > 0:
        air = buffer.pop(0)
        for side in sides:
            if [air[0] + side[0], air[1] + side[1], air[2] + side[2]] in cubes:
                side_count += 1
            elif [air[0] + side[0], air[1] + side[1], air[2] + side[2]] not in visited \
                    and min_x <= air[0] + side[0] <= start_x \
                    and min_y <= air[1] + side[1] <= start_y\
                    and min_z <= air[2] + side[2] <= start_z:
                visited.append([air[0] + side[0], air[1] + side[1], air[2] + side[2]])
                buffer.append([air[0] + side[0], air[1] + side[1], air[2] + side[2]])

    return side_count


assert count_sides([[1,1,1], [2,1,1]]) == 10
assert count_sides(common.Loader.load_matrix(delimiter=',', numeric=True, filename='test')) == 64
print(f'Side count of droplet is {count_sides(common.Loader.load_matrix(delimiter=",", numeric=True))}')

assert count_surface(common.Loader.load_matrix(delimiter=',', numeric=True, filename='test')) == 58
print(f'Surface count of droplet is {count_surface(common.Loader.load_matrix(delimiter=",", numeric=True))}')