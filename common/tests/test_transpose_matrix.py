from common.utils import transpose_matrix
import unittest


class TestLoader(unittest.TestCase):

    def test_simple_case(self):
        assert transpose_matrix([[0, 1],[2, 3]]) == [[0, 2], [1, 3]]

