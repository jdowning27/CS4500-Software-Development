import unittest
from unittest.mock import MagicMock

from Fish.Common.state import State
from Fish.Common.player_data import PlayerData
from Fish.Common.color import Color
from Fish.Common.board import Board
from Fish.Common.move import Move
from Fish.Common.skip import Skip
from Fish.Remote.Proxies.remote_player_proxy import RemotePlayerProxy
from Fish.Remote.Proxies.json_sock import JSONSocket


class RemotePlayerProxyTest(unittest.TestCase):
    def setUp(self):
        self.state = State(
            [PlayerData(Color.RED), PlayerData(Color.BROWN), PlayerData(Color.WHITE)],
            Board(4, 4))
        self.json_sock = JSONSocket(None)
        self.json_sock.send_json = MagicMock()
        self.json_sock.recv_json = MagicMock()
        self.proxy_player = RemotePlayerProxy(self.json_sock)

    # __init__() ##########################################################
    def test_constructor(self):
        self.assertRaisesRegex(
            ValueError, "json_json_sock must be an instance of JSONStream",
            RemotePlayerProxy, None)

    # start() ##############################################################
    def test_start_pass(self):
        self.json_sock.recv_json.return_value = "void"
        self.proxy_player.start(True)
        self.json_sock.send_json.assert_called_once_with(["start", [True]])
        self.json_sock.recv_json.assert_called_once()

    def test_start_fail(self):
        self.json_sock.recv_json.return_value = False
        self.assertRaisesRegex(
            RuntimeError, "Player did not return 'void' to start method",
            self.proxy_player.start, True)
        self.json_sock.send_json.assert_called_once_with(["start", [True]])
        self.json_sock.recv_json.assert_called_once()

    # end() ##############################################################
    def test_end_pass(self):
        self.json_sock.recv_json.return_value = "void"
        self.proxy_player.end(True)
        self.json_sock.send_json.assert_called_once_with(["end", [True]])
        self.json_sock.recv_json.assert_called_once()

    def test_end_fail(self):
        self.json_sock.recv_json.return_value = False
        self.assertRaisesRegex(
            RuntimeError, "Player did not return 'void' to end method",
            self.proxy_player.end, True)
        self.json_sock.send_json.assert_called_once_with(["end", [True]])
        self.json_sock.recv_json.assert_called_once()

    # play_as() ##############################################################
    def test_play_as_pass(self):
        self.json_sock.recv_json.return_value = "void"
        self.proxy_player.play_as(Color.RED)
        self.json_sock.send_json.assert_called_once_with(["playing-as", [Color.RED]])
        self.json_sock.recv_json.assert_called_once()

    def test_play_as_fail(self):
        self.json_sock.recv_json.return_value = False
        self.assertRaisesRegex(
            RuntimeError, "Player did not return 'void' to play_as method",
            self.proxy_player.play_as, Color.RED)
        self.json_sock.send_json.assert_called_once_with(["playing-as", [Color.RED]])
        self.json_sock.recv_json.assert_called_once()

    # play_with() ##############################################################
    def test_play_with_pass(self):
        self.json_sock.recv_json.return_value = "void"
        self.proxy_player.play_with([Color.BROWN, Color.WHITE])
        self.json_sock.send_json.assert_called_once_with(
            ["playing-with", [[Color.BROWN, Color.WHITE]]])
        self.json_sock.recv_json.assert_called_once()

    def test_play_with_fail(self):
        self.json_sock.recv_json.return_value = False
        self.assertRaisesRegex(
            RuntimeError, "Player did not return 'void' to play_with method",
            self.proxy_player.play_with, [Color.BROWN, Color.WHITE])
        self.json_sock.send_json.assert_called_once_with(
            ["playing-with", [[Color.BROWN, Color.WHITE]]])
        self.json_sock.recv_json.assert_called_once()

    # setup() ##############################################################
    def test_setup_pass(self):
        self.json_sock.recv_json.return_value = (0, 0)
        result = self.proxy_player.setup(self.state)
        self.assertEqual((0, 0), result)
        self.json_sock.send_json.assert_called_once_with(["setup", [self.state]])
        self.json_sock.recv_json.assert_called_once()

    def test_setup_fail(self):
        self.json_sock.recv_json.return_value = ("1", "0")
        self.assertRaisesRegex(
            RuntimeError, "Player did not return a int, int tuple to setup method",
            self.proxy_player.setup, self.state)
        self.json_sock.send_json.assert_called_once_with(["setup", [self.state]])
        self.json_sock.recv_json.assert_called_once()

    # tt() ##############################################################
    def test_tt_move_pass(self):
        self.json_sock.recv_json.return_value = Move((0, 0), (0, 2))
        result = self.proxy_player.tt(self.state, [])
        self.assertEqual(Move((0, 0), (0, 2)), result)
        self.json_sock.send_json.assert_called_once_with(["take-turn", [self.state, []]])
        self.json_sock.recv_json.assert_called_once()

    def test_tt_skip_pass(self):
        self.json_sock.recv_json.return_value = Skip()
        result = self.proxy_player.tt(self.state, [])
        self.assertEqual(Skip(), result)
        self.json_sock.send_json.assert_called_once_with(["take-turn", [self.state, []]])
        self.json_sock.recv_json.assert_called_once()

    def test_tt_fail(self):
        self.json_sock.recv_json.return_value = ((0, 0), ("1", "0"))
        self.assertRaisesRegex(
            RuntimeError, "Player did not return an Action to tt method",
            self.proxy_player.tt, self.state, [])
        self.json_sock.send_json.assert_called_once_with(["take-turn", [self.state, []]])
        self.json_sock.recv_json.assert_called_once()
