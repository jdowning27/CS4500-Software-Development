import unittest
from Fish.Common.util import *

class UtilTestCase(unittest.TestCase):
    def test_validate_int_valid(self):
        validate_int(5)
        validate_int(-7)
        validate_int(0)

    def test_validate_int_invalid(self):
        with self.assertRaises(SystemExit) as cm:
            validate_int("hello world")
            self.assertEqual(cm.exception.code, 1)

    def test_validate_non_neg_int_valid(self):
        validate_non_neg_int(0)
        validate_non_neg_int(5)

    def test_validate_non_neg_int_invalid(self):
        with self.assertRaises(SystemExit) as cm:
            validate_non_neg_int(-5)
            self.assertEqual(cm.exception.code, 1)

    def test_validate_pos_int_valid(self):
        validate_pos_int(5)

    def test_validate_pos_int_invalid(self):
        with self.assertRaises(SystemExit) as cm:
            validate_pos_int(0)
            self.assertEqual(cm.exception.code, 1)

    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(1))

    def test_print_test(self):
        with self.assertRaises(SystemExit) as cm:
            print_error("hello world")
            self.assetEqual(cm.exception.code, 1)
