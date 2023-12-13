import common
from colorama import Fore, Back, Style


def is_reflection(map, row_idx):
    max_reflection = min(len(map) - row_idx - 1, row_idx + 1)
    if max_reflection <= 0:
        return False
    for i in range(max_reflection):
        if map[row_idx + i + 1] != map[row_idx - i]:
            return False
    return True


class Map:
    def __init__(self, lines):
        self.map = [[ch for ch in line] for line in lines]
        self.transposed_map = common.transpose_matrix(self.map)
        self.row = 0
        self.column = 0
        self.row, self.column = self.find_reflection()

    def find_reflection(self):
        _row = 0
        _column = 0
        for i in range(len(self.map)):
            if is_reflection(self.map, i):
                if (i + 1) != self.row:
                    _row = i + 1
        for i in range(len(self.transposed_map)):
            if is_reflection(self.transposed_map, i):
                if (i + 1) != self.column:
                    _column = i + 1
        return _row, _column

    def swap(self, i, j):
        new = '#' if self.map[i][j] == '.' else '.'
        self.map[i][j] = new
        self.transposed_map[j][i] = new

    def find_smudge(self):
        _row = 0
        _column = 0
        # try to change all tiles and find reflection
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.swap(i, j)
                _new_row, _new_column = self.find_reflection()
                _row = max(_new_row, _row)
                _column = max(_new_column, _column)
                self.swap(i, j)
        self.row = _row
        self.column = _column

    def get_value(self, smudge=False):
        if smudge:
            self.find_smudge()
        # index of column where reflection "ends"
        # index of row where reflection "ends" * 100
        return self.column + self.row * 100

    def __repr__(self):
        return '\n'.join([''.join(line) for line in self.map]) + '\n'

    def __str__(self):
        return self.__repr__()


def compute_sum(maps, smudge=False):
    return sum([_.get_value(smudge) for _ in maps])


assert compute_sum(common.Loader.transform_lines_complex(Map, filename='test')) == 405

print(f'Part 1: {Back.GREEN}{Fore.BLACK}{compute_sum(common.Loader.transform_lines_complex(Map))}')

assert compute_sum(common.Loader.transform_lines_complex(Map, filename='test'), True) == 400

print(f'Part 2: {Back.GREEN}{Fore.BLACK}{compute_sum(common.Loader.transform_lines_complex(Map), True)}')