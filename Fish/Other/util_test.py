import unittest
from unittest.mock import MagicMock
from time import sleep
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

    def test_safe_call_timeout(self):
        self.assertFalse(safe_call(0.5, sleep, [1]))
        self.assertIsNone(safe_call(1, sleep, [0.5]))

    def test_safe_call_return(self):
        results = [
            ["test", 123],
            None,
            123,
            "test",
            True
        ]
        for result in results:
            self.assertEqual(safe_call(1, MagicMock(return_value=result)), result)

    def test_safe_call_exception(self):
        def bad_func():
            raise Exception
        self.assertFalse(safe_call(0.5, bad_func))

    # Testing is_posn ######################################################
    def test_is_posn_vaild(self):
        good_posns = [
            (0, 0),
            (1, 1),
            (-1, 0),
            (0, -1),
            (1234, 5678)
        ]
        for posn in good_posns:
            self.assertTrue(is_posn(posn))

    def test_is_posn_invalid(self):
        not_posns = [
            "test",
            1234,
            (1, 2, 3),
            (1),
            None,
            (" ", -1234),
            ((1, 2), 5),
            (0, "string")
        ]
        for posn in not_posns:
            self.assertFalse(is_posn(posn))

    def test_is_json_action_vaild(self):
        good_actions = [
            ((0, 0), (1, 0)),
            [[0, 0], [1, 0]],
            False
        ]
        for action in good_actions:
            self.assertTrue(is_json_action(action))

    def test_is_json_action_invalid(self):
        not_actions = [
            "test",
            1234,
            (1, 2, 3),
            (1),
            None,
            (" ", -1234),
            ((1, 2), 5),
            (0, "string")
        ]
        for action in not_actions:
            self.assertFalse(is_json_action(action))
