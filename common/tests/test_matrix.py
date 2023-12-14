from common.utils import transpose_matrix, rotate_matrix_ccw, rotate_matrix_cw
import unittest


class TestLoader(unittest.TestCase):

    def test_simple_case(self):
        assert transpose_matrix([[0, 1],[2, 3]]) == [[0, 2], [1, 3]]

    def test_rotate_ccw(self):
        assert rotate_matrix_ccw([[0, 1, 2], [3, 4, 5], [6, 7, 8]]) == [[2, 5, 8], [1, 4, 7], [0, 3, 6]]

    def test_rotate_cw(self):
        assert rotate_matrix_cw([[0, 1 ,2], [3, 4, 5], [6, 7, 8]]) == [[6, 3, 0], [7, 4, 1], [8, 5, 2]]

