import common
from colorama import Fore, Back, Style
import plotly.graph_objects as go
import networkx as nx
import numpy as np


def is_crossroad(_map, x, y):
    if y == len(_map) - 1:
        return True # end
    if sum([1 for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)] if 0 <= y < len(_map) and 0 <= x < len(_map[0]) and _map[y + dy][x + dx] not in ['#', 'X']]) > 1:
        return True


def convert_map(_map, can_climb_slopes=True):
    # convert to nodes and paths
    # find start
    start = (_map[0].index('.'), 0)
    _map[start[1]][start[0]] = 'X' # mark as visited
    # find end
    end = (_map[-1].index('.'), len(_map) - 1)

    # initialize parts
    node_map = {start: []}

    # format of buffer is "where I go from, where I am and how many steps"
    buffer = [(start, start[0], start[1]+1, 1, True, True)]
    while len(buffer) > 0:
        origin, where_x, where_y, steps, there, back = buffer.pop()
        _map[where_y][where_x] = 'X' # mark as visited
        if is_crossroad(_map, where_x, where_y) or (where_x, where_y) in node_map:
            # save path and "split"
            if (where_x, where_y) not in node_map:
                node_map[(where_x, where_y)] = []
            if back or can_climb_slopes:
                node_map[(where_x, where_y)].append((origin, steps))
            if there or can_climb_slopes:
                node_map[origin].append(((where_x, where_y), steps))
            origin = (where_x, where_y)
            there = True
            back = True
            steps = 0
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            x, y = where_x + dx, where_y + dy
            if x < 0 or y < 0 or x >= len(_map[0]) or y >= len(_map):
                continue
            if _map[y][x] not in ['#', 'X'] or (x, y) in node_map:
                if (x, y) != origin:
                    if ((_map[y][x] == '<' and dx == -1) or (_map[y][x] == '>' and dx == 1)
                            or (_map[y][x] == '^' and dy == -1) or (_map[y][x] == 'v' and dy == 1)):
                        buffer.append((origin, x, y, steps + 1, there, False))
                    elif ((_map[y][x] == '<' and dx == 1) or (_map[y][x] == '>' and dx == -1)
                            or (_map[y][x] == '^' and dy == 1) or (_map[y][x] == 'v' and dy == -1)):
                        buffer.append((origin, x, y, steps + 1, False, back))
                    else:
                        buffer.append((origin, x, y, steps + 1, there, back))

    return start, end, node_map


def find_path(_map, can_climb_slopes=True):
    start, end, node_map = convert_map(_map, can_climb_slopes)

    paths = [Path(start, [start], 0)]
    visited = {}
    counter = 0
    end_path = Path(None, [], 0)
    while len(paths) > 0:
        path = paths.pop()
        if path.hash() in visited and visited[path.hash()] > path.steps:
            continue
        visited[path.hash()] = path.steps

        for node, steps in node_map[path.where]:
            if node not in path.seen:
                if node == end:
                    counter += 1
                    if path.steps + steps > end_path.steps:
                        end_path = Path(node, path.seen + [node], path.steps + steps)
                else:
                    paths.append(Path(node, path.seen + [node], path.steps + steps))
        print(f'Visited {counter}, longest so far is {end_path.steps}')
    return end_path.steps


class Path:
    def __init__(self, where, seen, steps=1):
        self.where = where
        self.seen = seen
        self.steps = steps

    def hash(self):
        return f'{self.where}#{sorted(self.seen)}'


assert find_path(common.Loader.load_matrix('test'), can_climb_slopes=False) == 94
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{find_path(common.Loader.load_matrix(), can_climb_slopes=False)}')

# This won't work, I will have to find "crossroads" (paths with more then 2 '.' next to it
# and then navigate just this graph, otherwise I have too many paths going on at the same time :(
assert find_path(common.Loader.load_matrix('test')) == 154
print(f'Part 2: {Back.GREEN}{Fore.BLACK}{find_path(common.Loader.load_matrix())}')

# Did not finish, I just used "run long enough and get the longest path at that point" approach