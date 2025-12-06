from common.loader import Loader
import unittest


class TestLoader(unittest.TestCase):

    def test_load_matrix_keep_whitespaces(self):
        matrix = Loader.load_matrix('data/matrix_keep_whitespaces.txt', strip=False)
        result = [[' ', '1', '2', '3'], ['1', ' ', '2', ' ', '3'], ['1', ' ', '2', '3'], [' ', ' ', '1', ' ', ' '],['4', ' ', '5', ' ']]
        assert matrix == result

    def test_load_matrix_nums(self):
        matrix = Loader.load_matrix('data/matrix_nums.txt', delimiter=' ', numeric=True)
        result = [[1, 2, 3, 4, 5], [11, 12, -5, 67, 24], [4, 3], [9, 9, 9, 9, 9, 9, 9, 9, 9]]
        assert matrix == result

    def test_load_matrix_nums_regex(self):
        matrix = Loader.load_matrix('data/matrix_nums_mixed_whitespace.txt', delimiter='\\s+', numeric=True)
        result = [[1, 2, 3, 4, 5], [11, 12, -5, 67, 24], [4, 3], [9, 9, 9, 9, 9, 9, 9, 9, 9]]
        assert matrix == result

    def test_load_matrix_chars(self):
        matrix = Loader.load_matrix('data/matrix_chars.txt')
        result = [[y for y in x] for x in ['BCDEFGH', '==', '|.....|', '|.../.|', '|../..|']]
        assert matrix == result

    def test_load_matrix_nums_empty(self):
        matrix = Loader.load_matrix('data/matrix_nums_empty.txt', numeric=True)
        result = [[1, 2, 3, 4], [4, 5, 3, 4], [], [1, 2], [1, 2], [], [5]]
        assert matrix == result

    def test_load_lines(self):
        matrix = Loader.load_lines('data/lines_nums.txt', numeric=True)
        result = [1, 2, 3, 5, 9, 21, 5, 6]
        assert matrix == result

    def test_load_nostrip(self):
        matrix = Loader.load_lines('data/lines_nostrip.txt', strip=False)
        result = ['   |  ', ' 12 34', '12AB  ', '      ', ' - - -', '- - - ']
        print(matrix)
        assert matrix == result
