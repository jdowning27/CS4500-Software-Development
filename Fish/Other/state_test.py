import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

import unittest
from unittest.mock import MagicMock
from state import *
from board import *
from player_data import PlayerData
from color import *
from move import *


class StateTestCase(unittest.TestCase):

    def setUp(self):
        self.board_full = Board(4, 3)
        self.board_full.create_board_without_holes(4)
        self.board_holes = Board(4, 3)
        self.board_holes.create_board_with_holes([(0,0), (1,1)], 3)

        self.player1 = PlayerData(Color.RED, 5)
        self.player2 = PlayerData(Color.WHITE, 10)
        self.player3 = PlayerData(Color.BROWN)
        self.player4 = PlayerData(Color.BLACK)
        self.player5 = PlayerData(Color.BLACK) 
        self.players = [self.player1, self.player2]

        self.state_full = State(self.players, self.board_full)
        self.state_holes = State(self.players, self.board_holes)

    # init
    def test_too_few_players(self):
        self.assertRaisesRegex(ValueError, "Invalid number of players", State, [], self.board_full)

    def test_too_many_players(self):
        too_many_players = [self.player1, self.player2, self.player3, self.player4, self.player5]
        self.assertRaisesRegex(ValueError, "Invalid number of players", State, too_many_players, self.board_full)
    
    def test_duplicate_player_colors(self):
        duplicate_colors = [self.player1, self.player3, self.player4, self.player5]
        self.assertRaisesRegex(ValueError, "Players cannot have duplicate colors", State, duplicate_colors, self.board_full)

    def test_place_penguin_for_player_success(self):
        self.assertEqual(self.state_full.get_all_penguins(), [])
        new_state = self.state_full.place_penguin_for_player(Color.RED, (1, 2))
        self.assertEqual(new_state.get_all_penguins(), [(1, 2)])

    def test_place_penguin_for_player_out_of_bounds(self):
        self.assertEqual(self.state_full.get_all_penguins(), [])
        self.assertFalse(self.state_full.place_penguin_for_player(Color.RED, (4, 3)))
    
    def test_place_penguin_for_player_hole(self):
        self.assertEqual(self.state_holes.get_all_penguins(), [])
        self.assertFalse(self.state_holes.place_penguin_for_player(Color.RED, (0, 0)))

    def test_place_penguin_for_player_no_player(self):
        self.assertEqual(self.state_full.get_all_penguins(), [])
        self.assertFalse(self.state_full.place_penguin_for_player(Color.BROWN, (1, 2)))

    def test_get_all_penguins(self):
        self.assertEqual(self.state_full.get_all_penguins(), [])
        self.player1.get_penguins = MagicMock(return_value=[])
        self.player2.get_penguins = MagicMock(return_value=[(0,0), (3, 2)])
        self.assertEqual(self.state_full.get_all_penguins(), [(0,0), (3, 2)])

    def test_get_player_success(self):
        self.assertEqual(self.state_full.get_player(Color.RED), self.player1)
        self.assertEqual(self.state_full.get_player(Color.WHITE), self.player2)

    def test_get_player_no_player(self):
        self.assertFalse(self.state_full.get_player(Color.BROWN))

    def test_is_tile_available_true(self):
        self.assertTrue(self.state_full.is_tile_available((1, 1)))
        self.assertTrue(self.state_holes.is_tile_available((2, 2)))
    
    def test_is_tile_available_holes(self):
        self.assertFalse(self.state_holes.is_tile_available((0,0)))
        self.assertFalse(self.state_holes.is_tile_available((1,1)))

    def test_is_tile_available_out_of_bounds(self):
        self.assertFalse(self.state_full.is_tile_available((4, 3)))
        self.assertFalse(self.state_full.is_tile_available((-2, 3)))

    def test_is_tile_available_occupied(self):
        new_state = self.state_full.place_penguin_for_player(Color.RED, (1, 2))
        self.assertFalse(new_state.is_tile_available((1, 2)))
    
    def test_valid_move_success(self):
        self.state_full.get_all_penguins = MagicMock(return_value=[(0,0), (1, 0), (3, 2)])
        self.assertTrue(self.state_full.valid_move((0, 0), (2, 0)))

    def test_valid_move_occupied(self):
        self.state_full.get_all_penguins = MagicMock(return_value=[(0,0), (1, 0), (3, 2)])
        self.assertFalse(self.state_full.valid_move((0, 0), (1, 0)))

    def test_valid_move_hole(self):
        self.state_holes.get_all_penguins = MagicMock(return_value=[(0, 1), (1, 0), (3, 2)])
        self.assertFalse(self.state_holes.valid_move((0, 1), (1, 1)))
    
    def test_valid_move_no_penguin(self):
        self.state_holes.get_all_penguins = MagicMock(return_value=[(0, 1), (1, 0), (3, 2)])
        self.assertFalse(self.state_holes.valid_move((0, 0), (2, 0)))

    def test_valid_move_not_reachable(self):
        self.state_holes.get_all_penguins = MagicMock(return_value=[(0, 1), (1, 0), (3, 2)])
        self.assertFalse(self.state_holes.valid_move((0, 0), (3, 0)))

    def test_get_player_from_penguin_exists(self):
        self.player1.get_penguins = MagicMock(return_value=[(0,0), (1,0)])
        self.player2.get_penguins = MagicMock(return_value=[(3, 2)])
        self.assertEqual(self.state_full.get_player_from_penguin((3,2)), self.player2)

    def test_get_player_from_penguin_no_player(self):
        self.player1.get_penguins = MagicMock(return_value=[(0,0), (1,0)])
        self.assertFalse(self.state_full.get_player_from_penguin((3, 2)))

    def test_move_penguin_success(self):
        self.player1.add_penguin((0,0))

        self.assertTrue((0, 0) in self.state_full.get_all_penguins())
        self.assertFalse((2, 0) in self.state_full.get_all_penguins())
        self.assertEqual(self.state_full.get_current_player_color(), Color.RED)
        new_state = self.state_full.move_penguin((0, 0), (2, 0))
        self.assertTrue((2, 0) in new_state.get_all_penguins())
        self.assertFalse((0, 0) in new_state.get_all_penguins())
        self.assertEqual(new_state.get_current_player_color(), Color.WHITE)

    def test_move_penguin_occupied(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((2,0))
        self.assertEqual(self.state_full.get_all_penguins(), [(0, 0), (2, 0)])
        self.assertEqual(self.state_full.get_current_player_color(), Color.RED)
        self.assertFalse(self.state_full.move_penguin((0, 0), (2, 0)))
        self.assertEqual(self.state_full.get_all_penguins(), [(0, 0), (2, 0)])
        self.assertEqual(self.state_full.get_current_player_color(), Color.RED)

    def test_any_remaining_moves_true(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((2,0))
        self.assertTrue(self.state_full.any_remaining_moves())

    def test_any_remaining_moves_no_penguins(self):
        self.assertFalse(self.state_full.any_remaining_moves())

    def test_any_remaining_moves_no_moves(self):
        board = Board(4, 3)
        board.create_board_with_holes([(1, 0), (2, 0)], 0)
        state = State(self.players, board)
        self.player1.add_penguin((0,0))
        self.assertFalse(state.any_remaining_moves())

    def test_get_possible_moves(self):
        self.player1.add_penguin((0,0))

        actions = [Move((0,0), (1, 0)), Move((0,0), (2, 0)), Move((0,0), (2, 1)), Move((0,0), (3, 1))]
        for action in self.state_full.get_possible_moves():
            self.assertTrue(action in actions)
        self.assertEqual(len(self.state_full.get_possible_moves()), len(actions))

    def test_get_possible_moves_another_penguin(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((2, 1))
        actions = [Move((0,0), (1, 0)), Move((0,0), (2, 0))]
        for action in self.state_full.get_possible_moves():
            self.assertTrue(action in actions)
        self.assertEqual(len(self.state_full.get_possible_moves()), len(actions))

    def test_get_players_score_after_move(self):
        self.assertEqual(self.state_full.get_players_score(Color.RED), 0)
        self.player1.add_penguin((0,0))
        new_state = self.state_full.move_penguin((0,0), (1,0))
        self.assertEqual(new_state.get_players_score(Color.RED), 4)
        self.assertEqual(self.state_full.get_players_score(Color.WHITE), 0)


    def test_get_players_score_mutate_player(self):
        self.assertEqual(self.state_full.get_players_score(Color.RED), 0)
        self.player1.add_to_score(10)
        self.assertEqual(self.state_full.get_players_score(Color.RED), 10)
        
