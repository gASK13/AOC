import common
import re


class BingoField:
    def __init__(self, num):
        self.num = int(num)
        self.hit = False

    def __eq__(self, other):
        return other == self.num

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.num) + ("*" if self.hit else "")


class BingoBoard:
    def __init__(self, size):
        self.rows = []
        self.columns = [[] for i in range(size)]
        self.data = {}

    def parse_line(self, line):
        nums = [BingoField(x) for x in re.split('\\s+', line.strip())]
        self.rows.append(nums)
        for i in range(len(nums)):
            self.columns[i].append(nums[i])
            self.data[nums[i].num] = nums[i]

    def check(self, num):
        if num in self.data:
            self.data[num].hit = True
        for row in self.rows:
            if all([x.hit for x in row]):
                return self.unmarked_sum()
        for col in self.columns:
            if all([x.hit for x in col]):
                return self.unmarked_sum()
        return None

    def unmarked_sum(self):
        return sum([0 if self.data[i].hit else i for i in self.data])

    def __str__(self):
        s = "Board:\n"
        for x in self.rows:
            s += " ".join([str(i) for i in x])
            s += "\n"
        s += "\n"
        return s


#lines = common.Loader.load_lines('test.txt')
lines = common.Loader.load_lines()

data = [int(x) for x in lines.pop(0).split(',')]
matrices = []
while len(lines) > 0:
    lines.pop(0)
    matrix = BingoBoard(5)
    while len(lines) > 0 and len(lines[0]) > 0:
        matrix.parse_line(lines.pop(0))
    matrices.append(matrix)

while len(data) > 0 and len(matrices) > 0:
    curr = data.pop(0)
    for m in matrices:
        ret = m.check(curr)
        if ret is not None:
            print("Board won at {}".format(ret * curr))
    matrices = [m for m in matrices if m.check(0) is None]

