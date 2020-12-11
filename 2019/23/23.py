import copy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode import Parostroj

class Network:
    def __init__(self):
        self.queues = [[i] for i in range(0, 50)]
        self.nat = (0, 0)
        self.nat_delivered = 0
        self.idle = [0 for i in range(0, 50)]

    def is_idle(self):
        cnt = 0
        for i in self.idle:
            if i > 50:
                cnt += 1
        return cnt == 50

    def get_input(self, address):
        if self.is_idle():
            print('NAT ACTIVATED!')
            self.queues[0].append(self.nat[0])
            self.queues[0].append(self.nat[1])
            if self.nat_delivered == self.nat[1]:
                raise Exception('IT WAS {} ALL ALONG!'.format(self.nat_delivered))
            self.nat_delivered = self.nat[1]
            self.idle = [0 for i in range(0, 50)]

        if len(self.queues[address]) == 0:
            self.idle[address] += 1
            return -1
        else:
            return self.queues[address].pop(0)

    def get_output(self, address, x, y):
        # reset idle
        self.idle = [0 for i in range(0, 50)]

        if address == 255:
            print("NAT: {}@{}:{}".format(address, x, y))
            self.nat = (x, y)
        else:
            self.queues[address].append(x)
            self.queues[address].append(y)


program = open('23.txt', 'r').readline()
network = Network()
programs = []
for i in range(0, 50):
    programs.append(Parostroj(copy.deepcopy(program), input_provider=lambda i=i: network.get_input(i)))

i = 0
while True:
    programs[i].step()
    if len(programs[i].output) == 3:
        network.get_output(programs[i].output.pop(0), programs[i].output.pop(0), programs[i].output.pop(0))
    i += 1
    i = i % 50
