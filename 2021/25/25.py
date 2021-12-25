import common

class Map:
    def __init__(self, file=None):
        self.__map = {}
        matrix = common.Loader.load_matrix(file)
        self.__size = len(matrix[0]), len(matrix)
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] != '.':
                    self.__map[(x, y)] = matrix[y][x]

    def __step(self, x, y):
        if self.__map[(x, y)] == 'v':
            return x, (y + 1) % self.__size[1]
        else:
            return (x + 1) % self.__size[0], y

    def __cycle(self, char):
        new_map = {(x, y) : self.__map[(x, y)] for (x, y) in self.__map
                   if self.__map[(x, y)] != char or self.__step(x, y) in self.__map}
        moved = {self.__step(x, y): self.__map[(x, y)] for (x, y) in self.__map
                 if self.__map[(x, y)] == char and self.__step(x, y) not in self.__map}
        for x, y in moved:
            new_map[(x, y)] = moved[(x, y)]
        self.__map = new_map
        return len(moved)

    def cycle(self):
        return self.__cycle('>') + self.__cycle('v') > 0

    def run(self):
        i = 1
        while self.cycle():
            i += 1
        print(self)
        return i

    def __str__(self):
        visual = ''
        for y in range(self.__size[1]):
            visual += ''.join([self.__map[(x, y)] if (x, y) in self.__map else '.' for x in range(self.__size[0])]) + '\n'
        return visual


assert Map('test.txt').run() == 58
print(f'Real pt #1 {Map().run()}')

