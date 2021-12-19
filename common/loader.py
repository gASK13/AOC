import re
import os
import __main__
from aocd import get_data


class Loader:

    @staticmethod
    def transform_lines(transformer, filename=None):
        return [transformer(line=line) for line in Loader.load_lines(filename=filename)]

    @staticmethod
    def transform_lines_complex(transformer, limit='',filename=None):
        results = []
        lines = []
        for line in Loader.load_lines(filename=filename):
            if line == limit:
                results.append(transformer(lines=lines))
                lines = []
            else:
                lines.append(line)
        results.append(transformer(lines=lines))
        return results

    @staticmethod
    def load_lines(filename=None, numeric=False, strip=True):
        if filename is None:
            day = int(os.path.basename(__main__.__file__).split('.')[0])
            year = (os.path.basename(os.path.dirname(os.path.dirname(__main__.__file__))))
            data = get_data(day=day, year=year).splitlines()
            return [int(x) for x in data] if numeric else data
        with open(filename, 'r') as file:
            if numeric:
                return [int(x.strip()) for x in file.readlines()]
            return [x.strip() if strip else x.strip('\n') for x in file.readlines()]

    @staticmethod
    def load_matrix(filename=None, delimiter=None, numeric=False):
        matrix = []
        for line in Loader.load_lines(filename):
            if delimiter is None:
                split = line.strip()
            else:
                split = re.split(delimiter, line.strip())
            matrix.append([int(x) if numeric else x for x in split])
        return matrix
