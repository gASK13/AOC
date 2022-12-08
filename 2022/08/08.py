import common


def all_smaller(height, others):
    if len(others) == 0:
        return True
    others.sort()
    return others.pop() < height


def get_distance(height, others):
    dist = 0
    while len(others) > 0:
        if others[-1] < height:
            dist += 1
            others.pop()
        else:
            dist += 1
            break
    return dist


def find_visible_trees(trees):
    visible = []
    for x in range(len(trees[0])):
        for y in range(len(trees)):
            height = int(trees[y][x])
            can_be_seen = all_smaller(height, [int(i) for i in trees[y][:x]])
            can_be_seen |= all_smaller(height, list(reversed([int(i) for i in trees[y][x+1:]])))
            can_be_seen |= all_smaller(height, [int(line[x]) for line in trees[:y]])
            can_be_seen |= all_smaller(height, list(reversed([int(line[x]) for line in trees[y+1:]])))
            if can_be_seen:
                visible.append(height)
    return visible


def highest_scenic_score(trees):
    score = 0
    for x in range(len(trees[0])):
        for y in range(len(trees)):
            height = int(trees[y][x])
            distance = get_distance(height, [int(i) for i in trees[y][:x]])
            distance *= get_distance(height, list(reversed([int(i) for i in trees[y][x + 1:]])))
            distance *= get_distance(height, [int(line[x]) for line in trees[:y]])
            distance *= get_distance(height, list(reversed([int(line[x]) for line in trees[y + 1:]])))
            if distance > score:
                score = distance
    print(score)
    return score


assert len(find_visible_trees(common.Loader.load_lines('test'))) == 21
print(f'Visible trees: {len(find_visible_trees(common.Loader.load_lines()))}')

assert highest_scenic_score(common.Loader.load_lines('test')) == 8
print(f'Scenic score: {highest_scenic_score(common.Loader.load_lines())}')