import common
from colorama import Fore, Back

_DEBUG = False

class FileSystem():
    def __init__(self, line):
        self.line = line
        self.expanded = []
        blockId = 0
        is_block = True
        self.first = None
        self.last = None
        for item in line:
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

    def compact_step(self):
        self.expanded[self.first] = self.expanded[self.last]
        self.expanded[self.last] = -1
        while self.expanded[self.first] != -1:
            self.first += 1
        while self.expanded[self.last] == -1:
            self.last -= 1
        if _DEBUG:
            print(self)
        return self.last > self.first

    def compact(self):
        while self.compact_step():
            pass

    def checksum(self):
        return sum([idx*item for idx, item in enumerate(self.expanded) if item != -1])


def part_one(line):
    fs = FileSystem(line)
    fs.compact()
    return fs.checksum()

assert part_one('12355') == 60
assert part_one('2333133121414131402') == 1928
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{part_one(common.Loader.load_lines()[0])}{Fore.RESET}{Back.RESET}')

