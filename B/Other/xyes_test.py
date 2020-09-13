import unittest
from io import StringIO
from unittest.mock import patch
import xyes

class xyesTestCase(unittest.TestCase):
    def test_concat(self):
        self.assertEqual(xyes.concat(["a", "b", "c", "d"]), "a b c d")

    def test_concat_one(self):
        self.assertEqual(xyes.concat(["hello"]), "hello")

    def test_concat_empty(self):
        self.assertEqual(xyes.concat([]), "")

    def test_print_with_limit(self):
        str = "a b c d\n"
        expected_output = str*20

        with patch('sys.stdout', new = StringIO()) as producedOut:
            xyes.printSTDOUT("a b c d", 20)
            self.assertEqual(producedOut.getvalue(), expected_output)

