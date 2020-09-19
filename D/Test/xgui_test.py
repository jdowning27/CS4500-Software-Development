import unittest
from Other import xgui

class xGuiTestCase(unittest.TestCase):
    # no input
        # too many input
    # wrong type
    # less than/equal to 0
    # correct
    def test_no_input(self):
        with self.assertRaises(Exception):
           xgui.verify_input([])
    def test_too_many(self):
        with self.assertRaises(Exception):
            xgui.verify_input(['100', 'hello', 'world'])
    def test_wrong_type(self):
        with self.assertRaises(Exception):
            xgui.verify_input(['a string'])
    def test_decimal(self):
        with self.assertRaises(Exception):
            xgui.verify_input(['13.2'])
    def test_negative(self):
        with self.assertRaises(Exception):
            xgui.verify_input(['-123'])
    def test_zero(self):
        with self.assertRaises(Exception):
            xgui.verify_input(['0'])
    def test_success(self):
        self.assertEqual(xgui.verify_input(['400']), 400)
        self.assertEqual(xgui.verify_input(['1']), 1)
