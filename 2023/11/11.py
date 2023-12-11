import common

class Universe:
    def __init__(self, matrix):
        self.matrix = matrix

        # find all galaxies
        self.galaxies = []
        num = 1
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] == '#':
                    self.galaxies.append((x, y, num))
                    num += 1

        # find all empty rows and columns
        self.empty_rows = [y for y in range(len(self.matrix)) if all([self.matrix[y][x] == '.' for x in range(len(self.matrix[y]))])]
        self.empty_cols = [x for x in range(len(self.matrix[0])) if all([self.matrix[y][x] == '.' for y in range(len(self.matrix))])]

    def compute_distance(self, p1, p2, expansion):
        (x1, y1, _) = p1
        (x2, y2, _) = p2
        return (abs(x1 - x2) + abs(y1 - y2)
                + sum([expansion-1 for y in self.empty_rows if min(y1, y2) < y < max(y1, y2)])
                + sum([expansion-1 for x in self.empty_cols if min(x1, x2) < x < max(x1, x2)]))

    def get_distances(self, expansion=2):
        distance = 0
        for i in range(len(self.galaxies)):
            for j in range(i + 1, len(self.galaxies)):
                distance += self.compute_distance(self.galaxies[i], self.galaxies[j], expansion)
        return distance


assert Universe(common.Loader.load_matrix('test')).get_distances() == 374
assert Universe(common.Loader.load_matrix('test')).get_distances(10) == 1030
assert Universe(common.Loader.load_matrix('test')).get_distances(100) == 8410
print(f'Part 1: {Universe(common.Loader.load_matrix()).get_distances()}')
print(f'Part 2: {Universe(common.Loader.load_matrix()).get_distances(1000000)}')


