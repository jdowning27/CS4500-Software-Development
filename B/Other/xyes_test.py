import unittest
from io import StringIO
from unittest.mock import patch, Mock
from Other import xyes
import signal
import builtins

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

        with patch('sys.stdout', new = StringIO()) as produced_out:
            xyes.printSTDOUT("a b c d", 20)
            self.assertEqual(produced_out.getvalue(), expected_output)

    def handler(self, signum, frame):
        raise Exception("time out")

    def test_no_limit(self):
        one_sec, two_sec = [0, 0]
        with patch('builtins.print') as mock_print:
            signal.signal(signal.SIGALRM, self.handler)
            signal.alarm(1)
            try:
                xyes.printSTDOUT("hello")
            except Exception:
                one_sec = mock_print.call_count

        with patch('builtins.print') as mock_print_long:
            signal.signal(signal.SIGALRM, self.handler)
            signal.alarm(2)
            try:
                xyes.printSTDOUT("hello")
            except Exception:
                two_sec = mock_print_long.call_count
        
        self.assertTrue(two_sec > one_sec)
