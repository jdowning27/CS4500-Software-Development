import unittest
from unittest.mock import MagicMock


from Fish.Remote.Proxies.json_stream import JSONStream


class Dummy():
    pass


class ServerProxyTest(unittest.TestCase):

    def setUp(self):
        self.rfile, self.wfile = Dummy(), Dummy()
        self.json_stream = JSONStream(self.rfile, self.wfile)

    def test_send_json(self):
        self.wfile.write = MagicMock()
        self.json_stream.send_json([{'this': 'is'}, 1, "test"])
        self.wfile.write.assert_called_once_with('[{"this": "is"}, 1, "test"]')

    def test_recv_json(self):
        self.rfile.read = MagicMock()
        stream = '[{"this": "is"}, 1, "test"]truefalse{"help":911}[]'
        self.rfile.read.side_effect = list(char for char in stream)
        outputs = [
            [{'this': 'is'}, 1, "test"],
            True,
            False,
            {'help': 911},
            []
        ]
        for output in outputs:
            self.assertEqual(output, self.json_stream.recv_json())


if __name__ == '__main__':
    unittest.main()
