import common

class Screen:
    def __init__(self):
        self._screen = [[0 for char in range(50)] for row in range(6)]

    def rotate_screen(self):
        self._screen = common.utils.transpose_matrix(self._screen)

    def run_commands(self, lines):
        for line in lines:
            self.parse_line(line)
        self.print()
        return self.count()

    def parse_line(self, line):
        if line.startswith('rect'):
            size = line.split(' ')[1].split('x')
            (x, y) = (int(size[0]), int(size[1]))
            self._screen = [[1 if row < y and char < x else self._screen[row][char] for char in range(50)] for row in range(6)]
        else:
            if line.startswith('rotate column'):
                self.rotate_screen()
            # magic
            items = line.split('=')[1].split(' by ')
            row = int(items[0])
            column = int(items[1])
            self._screen[row] = self._screen[row][-column:] + self._screen[row][:-column]
            if line.startswith('rotate column'):
                self.rotate_screen()

    def get(self):
        return self._screen

    def count(self):
        return sum([sum(row) for row in self._screen])

    def print(self):
        print('\n'.join([''.join(['#' if ch == 1 else ' ' for ch in line]) for line in self._screen]))


assert Screen().run_commands(common.Loader.load_lines("test.txt")) == 6
print(f'Pixels ON are {Screen().run_commands(common.Loader.load_lines())}')


