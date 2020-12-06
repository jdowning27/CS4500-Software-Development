import unittest
from unittest.mock import MagicMock, call

from Fish.Common.state import State
from Fish.Common.player_data import PlayerData
from Fish.Common.color import Color
from Fish.Common.board import Board
from Fish.Common.move import Move
from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface
from Fish.Remote.Proxies.server_proxy import ServerProxy
from Fish.Remote.Proxies.json_sock import JSONSocket


class ServerProxyTest(unittest.TestCase):

    def setUp(self):
        self.state = State(
            [PlayerData(Color.RED), PlayerData(Color.BROWN), PlayerData(Color.WHITE)],
            Board(4, 4))

        self.json_sock = JSONSocket(None, None)

        self.player = LogicalPlayerInterface()

        self.player.start = MagicMock()
        self.player.end = MagicMock()
        self.player.play_as = MagicMock()
        self.player.play_with = MagicMock()

        self.posn = (0, 0)
        self.player.setup = MagicMock(return_value=self.posn)

        self.move = Move((0, 0), (1, 0))
        self.player.tt = MagicMock(return_value=self.move)

        self.server_proxy = ServerProxy(self.player, self.json_sock)

    def test_constructor(self):
        ServerProxy(self.player, self.json_sock)
        with self.assertRaises(ValueError):
            ServerProxy(self.player, None)
        with self.assertRaises(ValueError):
            ServerProxy(None, self.json_sock)

    def test_listen(self):
        self.json_sock.send_json = MagicMock()
        self.json_sock.recv_json = MagicMock()
        self.json_sock.recv_json.side_effect = [
            ["start", [True]],
            ["playing-as", ["red"]],
            ["playing-with", [["red", "black"]]],
            ["setup", [self.state.print_json()]],
            ["take-turn", [self.state.print_json(), []]],
            ["end", [True]]
        ]
        self.server_proxy.listen()
        self.json_sock.send_json.assert_has_calls([
            call("void"),
            call("void"),
            call("void"),
            call(self.posn),
            call(self.move.print_json()),
            call("void")
        ])

    def test_start(self):
        request = ["start", [True]]
        self.server_proxy._ServerProxy__handle_request(request)
        request = ["start", [False]]
        self.assertEqual("void", self.server_proxy._ServerProxy__handle_request(request))
        self.player.start.assert_has_calls([call(True), call(False)])

    def test_end(self):
        request = ["end", [True]]
        self.server_proxy._ServerProxy__handle_request(request)
        request = ["end", [False]]
        self.assertEqual("void", self.server_proxy._ServerProxy__handle_request(request))
        self.player.end.assert_has_calls([call(True), call(False)])

    def test_play_as(self):
        request = ["playing-as", ["red"]]
        self.server_proxy._ServerProxy__handle_request(request)
        request = ["playing-as", ["black"]]
        self.assertEqual("void", self.server_proxy._ServerProxy__handle_request(request))
        self.player.play_as.assert_has_calls([call(Color.RED), call(Color.BLACK)])

    def test_play_with(self):
        request = ["playing-with", [["red", "black"]]]
        self.server_proxy._ServerProxy__handle_request(request)
        request = ["playing-with", [["white", "brown"]]]
        self.assertEqual("void", self.server_proxy._ServerProxy__handle_request(request))
        self.player.play_with.assert_has_calls([call([Color.RED, Color.BLACK]),
                                                call([Color.WHITE, Color.BROWN])])

    def test_setup(self):
        request = ["setup", [self.state.print_json()]]
        self.assertEqual(self.posn,
                         self.server_proxy._ServerProxy__handle_request(request))
        self.player.setup.assert_called_once_with(self.state)

    def test_tt(self):
        actions = [self.move.print_json()]
        request = ["take-turn", [self.state.print_json(), actions]]
        self.assertEqual(self.move.print_json(),
                         self.server_proxy._ServerProxy__handle_request(request))
        self.player.tt.assert_called_once_with(self.state, [self.move])


if __name__ == '__main__':
    unittest.main()
