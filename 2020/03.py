map = []

def count_trees_on_slope(map, slope_x, slope_y):
    wrap = len(map[0])
    posx = 0
    posy = 0

    tree_count = 0
    while posy < len(map):
        if posx >= wrap:
            posx -= wrap
        if map[posy][posx] == '#':
            tree_count += 1
        posy += slope_y
        posx += slope_x

    print("Right: " + str(slope_x) + ", Down: " + str(slope_y) + " = " + str(tree_count))
    return tree_count


for line in open('03.txt', 'r').readlines():
    map.append(line.rstrip())


res = 1
res *= count_trees_on_slope(map, 1, 1)
res *= count_trees_on_slope(map, 3, 1)
res *= count_trees_on_slope(map, 5, 1)
res *= count_trees_on_slope(map, 7, 1)
res *= count_trees_on_slope(map, 1, 2)
print(res)