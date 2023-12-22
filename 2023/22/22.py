import common
from colorama import Fore, Back, Style

class Brick:
    def __init__(self, line):
        # coords are min_x, min_y, min_z and max_x, max_y, max_z
        self.coords = [[int(x) for x in _.split(',')] for _ in line.split('~')]

        # safety net!
        assert [self.coords[0][i] <= self.coords[1][i] for i in range(3)] == [True, True, True]

        self.held_by = []
        self.holds = []
        self.resting = False

    def lay_on(self, on_top_of):
        self.resting = True
        if on_top_of is not None:
            height = self.coords[1][2] - self.coords[0][2]
            self.coords[0][2] = on_top_of.get_top() + 1
            self.coords[1][2] = self.coords[0][2] + height
            self.held_by.append(on_top_of)
            on_top_of.holds.append(self)
        else:
            # drop to "floor"
            self.coords[1][2] -= self.coords[0][2]
            self.coords[1][2] += 1
            self.coords[0][2] = 1

    def get_bottom(self):
        return self.coords[0][2]

    def get_top(self):
        return self.coords[1][2]

    def get_2d_overlaps(self, bricks):
        overlaps = []
        for brick in bricks:
            if self.coords[0][0] <= brick.coords[1][0] and self.coords[1][0] >= brick.coords[0][0]:
                if self.coords[0][1] <= brick.coords[1][1] and self.coords[1][1] >= brick.coords[0][1]:
                    overlaps.append(brick)
        return overlaps

    def __str__(self):
        return f'Brick: {self.coords}'

    def __repr__(self):
        return self.__str__()

    def can_be_removed(self):
        for brick in self.holds:
            if len(brick.held_by) == 1:
                return False
        return True

    def get_chain_reaction_falls(self):
        # not including self though!
        falls = 0
        falling = [self]
        to_process = [_ for _ in self.holds]
        to_process.sort(key=lambda x: x.get_bottom(), reverse=True)
        while len(to_process) > 0:
            brick = to_process.pop()
            if brick in falling:
                continue
            if all(_ in falling for _ in brick.held_by):
                # all below are falling, so count it, add to falling and add above to process
                falls += 1
                falling.append(brick)
                to_process += brick.holds
                to_process.sort(key=lambda x: x.get_bottom(), reverse=True)
        # don't count self!

        return len(falling) - 1


def solve_part1(bricks):
    fall_bricks(bricks)
    return sum([1 for brick in bricks if brick.can_be_removed()])


def solve_part2(bricks):
    fall_bricks(bricks)
    return sum([brick.get_chain_reaction_falls() for brick in bricks])


def fall_bricks(bricks):
    # order bricks by get_bottom
    _working_bricks = sorted(bricks, key=lambda x: x.get_bottom(), reverse=True)

    # layers by top of brick
    layers = {}

    # now take bricks from "bottom" and try to fall them as low as possible
    # for each check what it can rest on by overlapping by X and Y from top layer
    while len(_working_bricks) > 0:
        brick = _working_bricks.pop()

        # go layer by layer and find overlap
        for key in sorted(layers.keys(), reverse=True):
            overlaps = brick.get_2d_overlaps(layers[key])
            if len(overlaps) > 0:
                for overlap in overlaps:
                    brick.lay_on(overlap)
                break

        if not brick.resting:
            # if no overlap, lay on ground
            brick.lay_on(None)

        layers[brick.get_top()] = layers.get(brick.get_top(), [])
        layers[brick.get_top()].append(brick)


assert solve_part1(common.Loader.transform_lines(Brick, 'test')) == 5
print(f'Part 1: {Back.GREEN}{Fore.BLACK}{solve_part1(common.Loader.transform_lines(Brick))}')

assert solve_part2(common.Loader.transform_lines(Brick, 'test')) == 7
print(f'Part 2: {Back.GREEN}{Fore.BLACK}{solve_part2(common.Loader.transform_lines(Brick))}')
