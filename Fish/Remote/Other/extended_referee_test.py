import unittest
from unittest.mock import MagicMock

from Fish.Remote.Adapters.extended_referee import ExtendedReferee
from Fish.Player.player import Player
from Fish.Common.color import Color

class TestExtendedReferee(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(2)
        self.player2 = Player(2)
        self.player3 = Player(1)
        self.players = [self.player1, self.player2, self.player3]
        self.ref = ExtendedReferee()

    def test_play_with_method_called(self):
        self.player1.play_with = MagicMock()
        self.player2.play_with = MagicMock()
        self.player3.play_with = MagicMock()

        self.ref.play_game(self.players)

        self.player1.play_with.assert_called_once_with([Color.WHITE, Color.BROWN])
        self.player2.play_with.assert_called_once_with([Color.RED, Color.BROWN])
        self.player3.play_with.assert_called_once_with([Color.RED, Color.WHITE])

    def test_player_timeout(self):
        def slow_func():
            sleep(10)

        self.player1.play_with = slow_func
        self.player2.play_with = slow_func
        game_result = self.ref.play_game([self.player1, self.player2, self.player3])
        self.assertEqual(type(game_result), dict)
        self.assertEqual(game_result["winners"], [self.player3])
        self.assertEqual(game_result["kicked_players"], set([self.player1, self.player2]))

    def test_player_exception(self):
        def bad_func():
            raise Exception

        self.player1.play_with = bad_func
        self.player2.play_with = bad_func
        game_result = self.ref.play_game([self.player1, self.player2, self.player3])
        self.assertEqual(type(game_result), dict)
        self.assertEqual(game_result["winners"], [self.player3])
        self.assertEqual(game_result["kicked_players"], set([self.player1, self.player2]))

if __name__ == '__main__':
    unittest.main()
