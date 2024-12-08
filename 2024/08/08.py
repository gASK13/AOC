import common
from colorama import Fore, Back

class NodeMap:
    def __init__(self, matrix):
        self.matrix = matrix
        self.nodes = {}
        for idy, line in enumerate(matrix):
            for idx, item in enumerate(line):
                if item != '.':
                    if self.matrix[idy][idx] not in self.nodes:
                        self.nodes[self.matrix[idy][idx]] = []
                    self.nodes[self.matrix[idy][idx]].append((idx, idy))

    def count_antinodes(self):
        antinodes = set()
        for list in self.nodes.values():
            for i in range(len(list)):
                for j in range(i+1, len(list)):
                    dx = list[i][0] - list[j][0]
                    dy = list[i][1] - list[j][1]
                    for nx ,ny in [(list[i][0] + dx, list[i][1] + dy), (list[j][0] - dx, list[j][1] - dy)]:
                        if len(self.matrix[0]) > nx >= 0 and len(self.matrix) > ny >= 0:
                            antinodes.add((nx, ny))

        #print('\n'.join([''.join([f'{Fore.RED}#{Fore.RESET}' if (idx, idy) in antinodes else c for idx, c in enumerate(line)]) for idy, line in enumerate(self.matrix)]))
        return len(antinodes)


assert NodeMap(common.Loader.load_matrix("test")).count_antinodes() == 14
print(f'Part 1: {Fore.BLACK}{Back.GREEN}{NodeMap(common.Loader.load_matrix()).count_antinodes()}{Fore.RESET}{Back.RESET}')