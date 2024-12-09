import common
from colorama import Fore, Back

class FileSystem():
    def __init__(self, line):
        self.line = line
        self.expanded = []
        blockId = 0
        is_block = True
        self.first = None
        self.last = None
        self.last_file = None
        self.blocks = {}
        self.holes = []
        for item in line:
            # Part two markers
            if is_block:
                self.blocks[blockId] = (len(self.expanded), int(item))
                self.last_file = blockId
            else:
                self.holes.append((len(self.expanded), int(item)))

            # Part one markers
            for i in range(int(item)):
                if is_block:
                    self.last = len(self.expanded)
                    self.expanded.append(blockId)
                else:
                    self.first = len(self.expanded) if self.first is None else self.first
                    self.expanded.append(-1)
            blockId += 1 if is_block else 0
            is_block = not is_block

    def format_c(self, p, c):
        cc = '.' if c == -1 else str(c)
        if p == self.first or p == self.last:
            return f'{Fore.RED}{cc}{Fore.RESET}'
        return cc

    def __str__(self):
        return ''.join([self.format_c(p, c) for p, c in enumerate(self.expanded)])

    def __repr__(self):
        return self.__str__()

    def compact_block(self):
        self.expanded[self.first] = self.expanded[self.last]
        self.expanded[self.last] = -1
        while self.expanded[self.first] != -1:
            self.first += 1
        while self.expanded[self.last] == -1:
            self.last -= 1
        return self.last > self.first

    def compact_file(self):
        if self.last_file == 0:
            return False
        # take rightmost file and try to move it to next hole
        block_idx, len_to_fit = self.blocks[self.last_file]

        # find the right hole
        hole_idx = None
        for hid, h_data in enumerate(self.holes):
            if h_data[1] >= len_to_fit and h_data[0] < block_idx:
                hole_idx = hid
                break

        if hole_idx is not None:
            # shorten hole
            start = self.holes[hole_idx][0]
            len = self.holes[hole_idx][1]
            self.holes[hole_idx] = (start + len_to_fit, len - len_to_fit)
            # move blocks
            for i in range(len_to_fit):
                self.expanded[start + i] = self.last_file
                self.expanded[block_idx + i] = -1

        self.last_file -= 1
        return True

    def compact(self, method='block'):
        if method == 'block':
            while self.compact_block():
                pass
        elif method == 'file':
            while self.compact_file():
                pass

    def checksum(self):
        return sum([idx*item for idx, item in enumerate(self.expanded) if item != -1])


def part_one(line):
    fs = FileSystem(line)
    fs.compact()
    return fs.checksum()

def part_two(line):
    fs = FileSystem(line)
    fs.compact(method='file')
    return fs.checksum()

assert part_one('12355') == 60
assert part_one('2333133121414131402') == 1928
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines()[0])}{Fore.RESET}{Back.RESET}')

assert part_two('12355') == 92
assert part_two('2333133121414131402') == 2858
print(len(common.Loader.load_lines()[0]))
print(f'Part 2: {Fore.BLACK}{Back.GREEN}{part_two(common.Loader.load_lines()[0])}{Fore.RESET}{Back.RESET}')

# 8518174061514
# TOO HIGH!!!
