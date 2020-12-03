import unittest
from unittest.mock import MagicMock, call

from Fish.Common.action import Action
from Fish.Common.board import Board
from Fish.Common.color import Color
from Fish.Common.player_interface import PlayerInterface
from Fish.Common.state import State
from Fish.Player.player import Player
from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface
from Fish.Remote.Adapters.logical_to_legacy_player import LogicalToLegacyPlayer


class TestLogicalToLegacyPlayer(unittest.TestCase):

    def setUp(self):
        self.legacy_player = Player()
        self.adapter = LogicalToLegacyPlayer(self.legacy_player)

    def test_constructor(self):
        LogicalToLegacyPlayer(PlayerInterface())
        LogicalToLegacyPlayer(Player())
        with self.assertRaises(ValueError):
            LogicalToLegacyPlayer(LogicalPlayerInterface())
        with self.assertRaises(ValueError):
            LogicalToLegacyPlayer(None)

    def test_start(self):
        self.legacy_player.tournament_start = MagicMock()
        self.adapter.start(True)
        self.legacy_player.tournament_start.assert_called_once()
        self.adapter.start(False)
        self.assertEqual(2, self.legacy_player.tournament_start.call_count)

    def test_end(self):
        self.legacy_player.tournament_end = MagicMock()
        self.adapter.end(True)
        self.legacy_player.tournament_end.assert_called_once()
        self.adapter.end(False)
        self.legacy_player.tournament_end.assert_has_calls([call(True), call(False)])

    def test_play_as(self):
        for color in Color:
            self.adapter.play_as(color)
            self.assertEqual(color, self.legacy_player.get_color())

    def test_play_with(self):
        self.legacy_player.play_with = MagicMock()
        self.adapter.play_with(list(Color))
        self.legacy_player.play_with.assert_called_once()
        self.adapter.play_with([])
        self.legacy_player.play_with.assert_has_calls([call(list(Color)), call([])])

    def test_setup(self):
        self.legacy_player.choose_placement = MagicMock()
        state = State([], Board(3, 3))
        self.adapter.setup(state)
        self.legacy_player.choose_placement.assert_called_once_with(state)

    def test_tt(self):
        self.legacy_player.set_state = MagicMock()
        self.legacy_player.choose_next_move = MagicMock()
        state = State([], Board(3, 3))
        actions = [Action(), Action(), Action()]
        self.adapter.tt(state, actions)
        self.legacy_player.set_state.assert_called_once_with(state)
        self.legacy_player.choose_next_move.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
