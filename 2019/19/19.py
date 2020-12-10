import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode import Parostroj


def print_map(_map):
    for line in _map:
        print(''.join([item for item in line]))

class Holder:
    def __init__(self, size, offset=(0, 0)):
        self.last_val = (-1, size - 1)
        self.size = size
        self.offset = offset
        self.input_index = 1
        self.map = [['?' for i in range(0, size)] for j in range(0, size)]

    def get_input(self):
        if self.input_index == 1:
            self.input_index = 0
            temp_y = (self.last_val[1] + 1)
            self.last_val = (self.last_val[0] + temp_y // self.size, temp_y % self.size)
        else:
            self.input_index = 1
        return self.last_val[self.input_index] + self.offset[self.input_index]

    def process_output(self, output):
        self.map[self.last_val[1]][self.last_val[0]] = '.' if output == 0 else '#'

    def stop_check(self):
        return self.map[self.size - 1][self.size - 1] != '?'

    def count_affected(self):
        cnt = 0
        for line in self.map:
            for item in line:
                if item == '#':
                    cnt +=1
        return cnt

# PART ONE - done & skipping
state = Holder(1, offset=(1000, 824))
while not state.stop_check():
    Parostroj(open('19.txt', 'r').readline(), output_processor=state.process_output, input_provider=state.get_input).run()
print_map(state.map)
print('AFFECTED: {}'.format(state.count_affected()))


def check_field(program, x, y):
    return Parostroj(program).run(input_array=[x, y])[0]


def check_rectange(program, x, y):
    return check_field(program, x, y) + check_field(program, x, y + 99) + check_field(program, x + 99, y) + check_field(program, x + 99, y + 99)


# PART TWO - let's hug the edge!
program = open('19.txt', 'r').readline()
cur_x = 100
cur_y = 0

# find the edge - @ x 100, go down
while check_field(program, cur_x, cur_y) == 0:
    cur_y += 1

# now hug the edge and check
while True:
    print(cur_x, cur_y)
    if check_rectange(program, cur_x - 99, cur_y) == 4:
        print(cur_x, cur_y)
        break
    if check_field(program, cur_x + 1, cur_y) == 1:
        cur_x += 1
    elif check_field(program, cur_x, cur_y + 1) == 1:
        cur_y += 1
    else:
        raise Exception('WTF?')

# D'oh! subtract 99!
print((cur_x - 99) * 10000 + cur_y)
11000825