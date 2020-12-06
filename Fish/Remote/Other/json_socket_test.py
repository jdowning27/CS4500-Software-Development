import unittest
from unittest.mock import MagicMock


from Fish.Remote.Proxies.json_socket import JSONSocket


class Dummy():
    pass


class ServerProxyTest(unittest.TestCase):

    def setUp(self):
        self.sock = Dummy()
        self.json_sock = JSONSocket(self.sock)

    def test_send_json(self):
        self.sock.sendall = MagicMock()
        self.json_sock.send_json([{'this': 'is'}, 1, "test"])
        self.sock.sendall.assert_called_once_with('[{"this": "is"}, 1, "test"]'.encode())

    def test_recv_json(self):
        self.sock.recv = MagicMock()
        sock = '[{"this": "is"}, 1, "test"]truefalse{"help":911}[]'
        self.sock.recv.side_effect = list(char.encode() for char in sock)
        outputs = [
            [{'this': 'is'}, 1, "test"],
            True,
            False,
            {'help': 911},
            []
        ]
        for output in outputs:
            self.assertEqual(output, self.json_sock.recv_json())


if __name__ == '__main__':
    unittest.main()
