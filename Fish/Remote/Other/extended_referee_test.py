import unittest
from unittest.mock import MagicMock

from Fish.Remote.Adapters.extended_referee import ExtendedReferee
from Fish.Player.player import Player
from Fish.Common.color import Color

class TestExtendedReferee(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(2)
        self.player2 = Player(2)
        self.player3 = Player(2)
        self.players = [self.player1, self.player2, self.player3]

    def test_play_with_method_called(self):
        self.player1.play_with = MagicMock()
        self.player2.play_with = MagicMock()
        self.player3.play_with = MagicMock()

        ref = ExtendedReferee()
        ref.play_game(self.players)

        self.player1.play_with.assert_called_once_with([Color.WHITE, Color.BROWN])
        self.player2.play_with.assert_called_once_with([Color.RED, Color.BROWN])
        self.player3.play_with.assert_called_once_with([Color.RED, Color.WHITE])

if __name__ == '__main__':
    unittest.main()
