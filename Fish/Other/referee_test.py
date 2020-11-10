import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Player'
sys.path.append(os_path)
os_path = os.path.dirname(os.getcwd()) + '/Fish/Admin'
sys.path.append(os_path)


import unittest
from unittest import mock
from unittest.mock import patch
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
        self.ext_players = [self.player1, self.player2, self.player3]
        self.referee = Referee()

    def test_initialize_game(self):
        game = self.referee.initialize_game(self.ext_players)
        self.assertEqual(type(game), GameTree)
        self.assertEqual(len(game.state.get_all_penguins()), 9)
        self.assertEqual(self.player1.get_penguins(), {(0,0), (1,0), (2,0)})
        self.assertEqual(self.player2.get_penguins(), {(0,1), (1,1), (2,1)})
        self.assertEqual(self.player3.get_penguins(), {(0,2), (1,2), (2,2)})

        self.assertEqual(self.player1.get_color(), Color.RED)
        self.assertEqual(self.player2.get_color(), Color.WHITE)
        self.assertEqual(self.player3.get_color(), Color.BROWN)

        self.assertFalse(self.referee.has_game_ended())

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
        self.assertEqual(type(self.referee.play_game(self.ext_players)), GameEnded)
        self.assertEqual(self.referee.get_winners(), self.ext_players)

    # TODO: this mocking needs to change when we redo the Referee class
    # def test_play_game_invalid_move(self):
    #     with patch.object(Referee, "check_move_validity", return_value=False) as mock_validity:
    #         game_over = self.referee.play_game(self.ext_players)
    #         self.assertEqual(type(game_over), GameEnded)
    #         self.assertEqual(self.referee.get_winners(), [])
    #         self.assertEqual(self.referee.get_players(), [])


    def test_alert_winners(self):
        with patch.object(Player, "game_over") as mock_game_over:
            game_over = self.referee.play_game(self.ext_players)
            self.referee.alert_players()
        mock_game_over.assert_called()

    def test_alert_winners_no_winners(self):
        with patch.object(Player, "game_over") as mock_game_over:
            game = self.referee.initialize_game(self.ext_players)
            self.referee.alert_players()
        mock_game_over.assert_not_called()

    def test_next_turn(self):
        self.referee.initialize_game(self.ext_players)
        self.assertEqual(self.referee.get_players(), self.ext_players)
        self.referee.next_turn()
        self.assertEqual(self.referee.get_players(), [self.player2, self.player3, self.player1])

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

