import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Player'
sys.path.append(os_path)
os_path = os.path.dirname(os.getcwd()) + '/Fish/Admin'
sys.path.append(os_path)


import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from player import Player
from referee import Referee
from game_tree import GameTree
from color import Color
from move import Move
from game_ended import GameEnded

class RefereeTestCase(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(3)
        self.player2 = Player(5)
        self.player3 = Player(7)
        self.player4 = Player(1)
        self.player5 = Player(1)
        self.ext_players = [self.player1, self.player2, self.player3]
        self.referee = Referee()

    def test_initialize_game(self):
        game = self.referee.initialize_game(self.ext_players)
        self.assertEqual(type(game), GameTree)
        self.assertEqual(len(game.state.get_all_penguins()), 9)

        self.assertEqual(self.player1.get_color(), Color.RED)
        self.assertEqual(self.player2.get_color(), Color.WHITE)
        self.assertEqual(self.player3.get_color(), Color.BROWN)

        self.assertFalse(self.referee.has_game_ended())

    def test_initialize_game_player_kicked(self):
        self.player1.choose_placement = MagicMock(return_value=(-1, 0))
        game = self.referee.initialize_game(self.ext_players)
        self.assertEqual(self.referee.get_players_as_colors(), [Color.WHITE, Color.BROWN])

    def test_initialize_game_too_few_players(self):
        self.assertRaisesRegex(ValueError, "Invalid number of players", self.referee.initialize_game, [])

    def test_initialize_game_too_many_players(self):
        too_many_players = [self.player1, self.player2, self.player3, self.player4, self.player5]
        self.assertRaisesRegex(ValueError, "Invalid number of players", self.referee.initialize_game, too_many_players)

    def test_check_move_validity(self):
        game = self.referee.initialize_game(self.ext_players)
        game_tree = self.referee.check_move_validity(Move((2,0), (3,0)))
        self.assertEqual(type(game_tree), GameTree)

    def test_check_move_validity_false(self):
        game = self.referee.initialize_game(self.ext_players)
        self.assertFalse(self.referee.check_move_validity(Move((2,0), (1,0))))

    def test_check_move_validity_game_setup(self):
        self.assertFalse(self.referee.check_move_validity(Move((2,0), (3,0))))


    def test_play_game(self):
        game_result = self.referee.play_game(self.ext_players)
        self.assertEqual(type(game_result), dict)
        self.assertEqual(game_result["winners"], self.ext_players)
        self.assertEqual(game_result["kicked_players"], set())

    def test_play_game_player_kicked(self):
        self.player1.choose_next_move = MagicMock(return_value=Move((0,0), (1, 1)))
        game_result = self.referee.play_game(self.ext_players)
        self.assertEqual(game_result["winners"], [self.player2])
        self.assertEqual(game_result["kicked_players"], {self.player1})

    def test_alert_winners(self):
        with patch.object(Player, "game_over") as mock_game_over:
            game_result = self.referee.play_game(self.ext_players)
            self.referee.alert_players(game_result)
        mock_game_over.assert_called()

    def test_alert_winners_no_winners(self):
        with patch.object(Player, "game_over") as mock_game_over:
            game = self.referee.initialize_game(self.ext_players)
            self.referee.alert_players({})
        mock_game_over.assert_not_called()

    def test_get_winners(self):
        self.referee.play_game(self.ext_players)
        self.assertEqual(self.referee.get_winners(), self.ext_players)

    def test_get_winners_game_not_played(self):
        self.referee.initialize_game(self.ext_players)
        self.assertFalse(self.referee.get_winners())

    def test_get_current_scores(self):
        self.referee.initialize_game(self.ext_players)
        self.assertEqual(self.referee.get_current_scores(), [(self.player1, 0), (self.player2, 0), (self.player3, 0)])

    def test_has_game_ended(self):
        self.assertFalse(self.referee.has_game_ended())
        self.referee.play_game(self.ext_players)
        self.assertTrue(self.referee.has_game_ended())

