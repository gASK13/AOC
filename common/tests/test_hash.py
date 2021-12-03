from common.utils import *
import unittest


class TestLoader(unittest.TestCase):

    def test_hash_nums_default(self):
        assert hash_list([0, 1, 2, 3]) == '0#1#2#3'

    def test_hash_string_default(self):
        assert hash_list(['Ahoj', 'Cau', 'Nazdar']) == 'Ahoj#Cau#Nazdar'

    def test_hash_mixed_default(self):
        assert hash_list([0, 'Word', 5.6]) == '0#Word#5.6'

    def test_hash_nums_custom(self):
        assert hash_list([0, 1, 2, 3],delimiter='@%^&') == '0@%^&1@%^&2@%^&3'
