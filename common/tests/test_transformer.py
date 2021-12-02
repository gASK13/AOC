from common.loader import Loader
import unittest


class TestTransformer:
    def __init__(self, chr=None, nr_1=None, nr_2=None, line=None,):
        self.chr = line.split(' ')[0] if chr is None else chr
        self.nr_1 = int(line.split(' ')[1].split('#')[0]) if nr_1 is None else nr_1
        self.nr_2 = int(line.split(' ')[1].split('#')[1]) if nr_2 is None else nr_2

    def __eq__(self, other):
        return (self.chr == other.chr) & (self.nr_1 == other.nr_1) & (self.nr_2 == other.nr_2)


class TestLoader(unittest.TestCase):

    def test_load_matrix_nums(self):
        matrix = Loader.transform_lines(TestTransformer, 'data/trans_data.txt')
        result = [TestTransformer('A', 26, 1),
                  TestTransformer('B', 21, 2),
                  TestTransformer('C', 13, 3),
                  TestTransformer('D', 44, 4)]
        assert matrix == result

