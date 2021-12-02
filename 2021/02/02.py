from common.loader import Loader

class Action:
    def __init__(self, line):
        self.num = int(line.split(' ')[1])
        self.action = line.split(' ')[0]

    def apply_1(self, position):
        if self.action == 'up':
            return position[0] - self.num, position[1]
        if self.action == 'down':
            return position[0] + self.num, position[1]
        if self.action == 'forward':
            return position[0], position[1] + self.num

    def apply_2(self, position):
        if self.action == 'up':
            return position[0], position[1], position[2] - self.num
        if self.action == 'down':
            return position[0], position[1], position[2] + self.num
        if self.action == 'forward':
            return position[0] + self.num * position[2], position[1] + self.num, position[2]


actions = Loader.transform_lines(Action)
pos1 = (0, 0)
pos2 = (0, 0, 0)
for action in actions:
    pos1 = action.apply_1(pos1)
    pos2 = action.apply_2(pos2)

print(pos1[0] * pos1[1])
print(pos2[0] * pos2[1])
