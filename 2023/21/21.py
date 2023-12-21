import common
from colorama import Fore, Back, Style
import math

test_data = {6: 16, 10: 50, 50: 1594, 100: 6536, 500: 167004, 1000: 668697, 5000: 16733044}


def find_path_simple(_map, _steps):
    start_y = ['S' in _ for _ in _map].index(True)
    start_x = _map[start_y].index('S')
    return len(iterate_map(_map, _steps, [(start_x, start_y)])[0])


# copy map next to each other in X copies, replacing S with . except for middle one
def multiply_map(_map, copies):
    start_y = ['S' in _ for _ in _map].index(True)
    start_x = _map[start_y].index('S')
    _map[start_y][start_x] = '.'
    new_map = []
    for i in range(copies * 2 + 1):
        for line in _map:
            new_map.append('-'.join(['-'.join(line) for _ in range(copies * 2 + 1)]).split('-'))
    new_map[start_y + copies * len(_map[0])][start_x + copies * len(_map[1])] = 'S'
    return new_map


def find_path_simple_multiply(_map, _steps):
    new_map = multiply_map(_map, math.ceil(_steps / len(_map)))
    start_y = ['S' in _ for _ in new_map].index(True)
    start_x = new_map[start_y].index('S')
    positions, seen = iterate_map(new_map, _steps, [(start_x, start_y)])
    return len(positions)


def visualize_map(_map, positions, edge_positions):
    new_map = [['.' for _ in range(len(_map[0]) + 2)] for _ in range(len(_map) + 2)]
    for y in range(len(_map)):
        for x in range(len(_map[0])):
            new_map[y + 1][x + 1] = _map[y][x]
    for x, y in positions:
        new_map[y + 1][x + 1] = 'O'
    for x, y in edge_positions:
        new_map[y + 1][x + 1] = 'X'
    for line in new_map:
        print(''.join(line))
    print('')


def util_get_count(_map, _steps):
    start_y = ['S' in _ for _ in _map].index(True)
    start_x = _map[start_y].index('S')

    left_count, left_steps = iterate_map(_map, _steps, [(len(_map[0]), start_y)])
    right_count, right_steps = iterate_map(_map, _steps, [(-1, start_y)])
    up_count, up_steps = iterate_map(_map, _steps, [(start_x, len(_map))])
    down_count, down_steps = iterate_map(_map, _steps, [(start_x, -1)])

    left_up_count, left_up_steps = iterate_map(_map, _steps-1, [(len(_map[0]), len(_map) - 1)])
    left_down_count, left_down_steps = iterate_map(_map, _steps-1, [(len(_map[0]), 0)])
    right_up_count, right_up_steps = iterate_map(_map, _steps-1, [(0, len(_map))])
    right_down_count, right_down_steps = iterate_map(_map, _steps-1, [(-1, 0)])

    assert left_steps == right_steps == up_steps == down_steps
    assert left_up_steps == left_down_steps == right_up_steps == right_down_steps
    assert left_count == right_count == up_count == down_count
    assert left_up_count == left_down_count == right_up_count == right_down_count

    return len(left_count), left_steps, len(left_up_count), left_up_steps


def find_path_complex(_map, _steps):
    # check if we have vertical / horizontal path
    assert check_map(_map)
    start_y = ['S' in _ for _ in _map].index(True)
    start_x = _map[start_y].index('S')

    # I computed the constants using the method "util_get_count" and "find_path_simple" above
    # count > inital square count
    # odd and even_count is how many squares we can fill in odd and even number of steps on entrance (!)
    # since it takes 131 steps to traverse a square, we will alternate those in layers
    odd_count = 7627
    even_count = 7770
    steps_to_fill = 196  # 131 * 1.5

    # steps to fill is "how many steps do we need to fill the whole map" so entering with less then this needs special handling

    # to traverse the map, we can move in 4 directions, so steps = map width or height
    steps_to_traverse = len(_map[0])

    if _steps <= (steps_to_traverse // 2):
        # we can just use the simple method
        return find_path_simple(_map, _steps)
    elif _steps <= steps_to_traverse:
        # simple method when going only to the sides
        count = find_path_simple(_map, _steps)
        count += len(iterate_map(_map, _steps - (steps_to_traverse // 2), [(len(_map[0]), start_y)])[0])
        count += len(iterate_map(_map, _steps - (steps_to_traverse // 2), [(-1, start_y)])[0])
        count += len(iterate_map(_map, _steps - (steps_to_traverse // 2), [(start_x, len(_map))])[0])
        count += len(iterate_map(_map, _steps - (steps_to_traverse // 2), [(start_x, -1)])[0])
        return count


    # start with filled inner square
    left_steps = _steps - steps_to_traverse // 2
    count = odd_count if _steps % 2 == 1 else even_count
    layer_size = 4
    odd = left_steps % 2 == 1

    # let's try to iterate by layer
    while left_steps > steps_to_fill:
        count += layer_size * (odd_count if odd else even_count)
        left_steps -= steps_to_traverse
        odd = left_steps % 2 == 1
        layer_size += 4

    # now we have left over - fill each direction on its own!
    while left_steps > 0:
        # there will be 1 of each direct directions
        count += len(iterate_map(_map, left_steps, [(len(_map[0]), start_y)])[0])
        count += len(iterate_map(_map, left_steps, [(-1, start_y)])[0])
        count += len(iterate_map(_map, left_steps, [(start_x, len(_map))])[0])
        count += len(iterate_map(_map, left_steps, [(start_x, -1)])[0])

        # there will be layer_size - 4 / 4 of each diagonal direction
        # diagonals come after 65, not 131 (cause we go "by side")
        # also diagonals have to start "one of the edge" and thus "one step later"
        count += (layer_size - 4) // 4 * len(iterate_map(_map, left_steps + (steps_to_traverse // 2), [(len(_map[0]), len(_map) - 1)])[0])
        count += (layer_size - 4) // 4 * len(iterate_map(_map, left_steps + (steps_to_traverse // 2), [(len(_map[0]), 0)])[0])
        count += (layer_size - 4) // 4 * len(iterate_map(_map, left_steps + (steps_to_traverse // 2), [(0, len(_map))])[0])
        count += (layer_size - 4) // 4 * len(iterate_map(_map, left_steps + (steps_to_traverse // 2), [(-1, 0)])[0])

        # on to the next!
        left_steps -= steps_to_traverse
        layer_size += 4

    # If we have "negative steps" shorter then half side, we reached diagonals before we left
    if left_steps > -(steps_to_traverse // 2):
        count += (layer_size - 4) // 4 * len(
            iterate_map(_map, left_steps + (steps_to_traverse // 2), [(len(_map[0]), len(_map) - 1)])[0])
        count += (layer_size - 4) // 4 * len(
            iterate_map(_map, left_steps + (steps_to_traverse // 2), [(len(_map[0]), 0)])[0])
        count += (layer_size - 4) // 4 * len(
            iterate_map(_map, left_steps + (steps_to_traverse // 2), [(0, len(_map))])[0])
        count += (layer_size - 4) // 4 * len(iterate_map(_map, left_steps + (steps_to_traverse // 2), [(-1, 0)])[0])

    return count


def iterate_map(_map, _steps, starts):
    positions = set(starts)
    seen_counts = []
    for step in range(_steps):
        new_positions = set()
        for position in positions:
            for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = position[0] + x, position[1] + y
                if 0 <= new_x < len(_map[0]) and 0 <= new_y < len(_map):
                    if _map[new_y][new_x] != '#':
                        new_positions.add((new_x, new_y))
        positions = new_positions
        seen_counts.append(len(positions))
        # if the last 2 repeat for the first time, we can stop
        if len(seen_counts) > 4 and seen_counts[-1] == seen_counts[-3] and seen_counts[-2] == seen_counts[-4]:
            if (_steps - step) % 2 == 0:
                # we need to end on even remaining steps
                break

    return positions, len(
        seen_counts)  # seen count size == number of steps until we start repeating and fill the whole map


def check_map(_map):
    start_y = ['S' in _ for _ in _map].index(True)
    start_x = _map[start_y].index('S')

    return all([_map[start_y][_] != '#' for _ in range(len(_map[0]))]) and all(
        [_map[_][start_x] != '#' for _ in range(len(_map))])


assert find_path_simple(common.Loader.load_matrix('test'), 6) == 16

print(f'Part 1: {Back.GREEN}{Fore.BLACK}{find_path_simple(common.Loader.load_matrix(), 64)}')

# Verified, commented tests for "simple iteration"
# for steps, result in test_data.items():
#     actual = find_path_simple_multiply(common.Loader.load_matrix('test'), steps)
#     if actual != result:
#         print(f'{Fore.RED}For {steps} steps, result should be {result}, but is {actual}')
#     else:
#         print(f'For {steps} steps, result is matching {result}.')

# Verification code for "complex code" to verify it agains "complex"
for steps in [65, 66, 100, 131, 132, 133, 166, 194, 200, 212, 250, 259, 260, 261, 262, 267, 290, 300, 500]:
    simple = find_path_simple_multiply(common.Loader.load_matrix(), steps)
    complex = find_path_complex(common.Loader.load_matrix(), steps)
    if simple != complex:
        print(f'{Fore.RED}For {steps} steps, simple result should be {simple}, but is {complex}')
    else:
        print(f'For {steps} steps, simple result is matching complex at {simple}.')\

# UTILS
# print(find_path_simple(common.Loader.load_matrix(), 26501365))
# print(util_get_count(common.Loader.load_matrix(), 26501365))
# print(util_get_count(common.Loader.load_matrix(), 26501364))

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{find_path_complex(common.Loader.load_matrix(), 26501365)}')
print(f'If it\'s {Back.YELLOW}630129824772393{Fore.RESET}{Back.RESET}, GREAT!')

# Postmortem:
# - this took me too many tries, should have taken pen and paper sooner
# - I made too many stupid "off by one" errors
# - in the end I spent most of my time trying to figure out why my code is wrong and I had switched "odd" and "even" counts
# - should have relied on code instead of trying to save time with constants, duh!