import re


class Loader:

    @staticmethod
    def load_matrix(filename, delimiter=None, numeric=False):
        matrix = []
        with open(filename, 'r') as file:
            for line in file.readlines():
                if delimiter is None:
                    split = line.strip()
                else:
                    split = re.split(delimiter, line.strip())
                matrix.append([int(x) if numeric else x for x in split])
        return matrix

