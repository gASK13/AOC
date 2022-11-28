from common.loader import Loader
import common.utils


def compute_distance(steps, stop_twice=False):
    direction = (0, -1)
    distance = (0, 0)
    visited = {common.hash_list(distance): 0}
    for step in steps:
        if step[0] == 'R':
            direction = (-direction[1], direction[0])
        else:
            direction = (direction[1], -direction[0])
        for i in range(0, int(step[1:])):
            distance = (distance[0] + direction[0], distance[1] + direction[1])
            hash = common.hash_list(distance)
            if stop_twice and hash in visited:
                return abs(distance[0]) + abs(distance[1])
            visited[hash] = abs(distance[0]) + abs(distance[1])
    return abs(distance[0]) + abs(distance[1])


assert compute_distance(['R2', 'L3']) == 5
assert compute_distance(['R2', 'R2', 'R2']) == 2
assert compute_distance(['R5', 'L5', 'R5', 'R3']) == 12
assert compute_distance(['R5', 'L500', 'R5', 'R3']) == 507
print(f"Distance to HQ is {compute_distance(Loader.load_matrix(delimiter=', ',numeric=False)[0])}")


assert compute_distance(['R8', 'R4', 'R4', 'R8'], True) == 4
print(f"Distance to proper HQ is {compute_distance(Loader.load_matrix(delimiter=', ',numeric=False)[0], True)}")