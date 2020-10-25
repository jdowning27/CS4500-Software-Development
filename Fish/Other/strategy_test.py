import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Player'
sys.path.append(os_path)

import unittest
from operator import le, ge

from strategy import find_minimax_action, place_penguin_across, choose_action_minimax
from game_tree import *
from State import *
from Board import *
from Player import *
from Color import *
from Move import *


class StrategyTestCase(unittest.TestCase):

    def setUp(self):
        self.board_full = Board(4, 3)
        board_array = [
            [1,     2,      3],
                [4,     3,      2],
            [3,     4,      1],
                [5,     2,      1]
        ]
        self.board_full.create_board_from_json(board_array)
        self.board_holes = Board(4, 3)
        self.board_holes.create_board_with_holes([(0, 0), (0, 1), (0, 2)], 3)

        self.player1 = Player(Color.RED, 5)
        self.player2 = Player(Color.WHITE, 10)
        self.players = [self.player1, self.player2]

        self.state_full = State(self.players, self.board_full)
        self.state_holes = State(self.players, self.board_holes)

        self.action1 = Move((0,0), (1,0))
        self.action2 = Move((2,0), (3,0))

        self.game_tree = GameTree(self.state_full)
        self.game_tree_holes = GameTree(self.state_holes)

        self.state1_0 = self.state_full.move_penguin((0,0), (1,0))
        self.state2_0 = self.state_full.move_penguin((0,0), (2,0))
        self.state2_1 = self.state_full.move_penguin((0,0), (2,1))
        self.state3_1 = self.state_full.move_penguin((0,0), (3,1))

    def test_find_minimax_action_score(self):
        action_score = find_minimax_action((self.action1, 8), (self.action2, 1), ge)
        self.assertEqual(action_score, (self.action1, 8))

    def test_find_minimax_action_row_ge(self):
        action_row = Move((1, 0), (1, 0))
        actual_action_score = find_minimax_action((self.action1, 2), (action_row, 2), ge)
        self.assertEqual(actual_action_score, (self.action1, 2))

    def test_find_minimax_action_col_ge(self):
        action_col = Move((3,0), (1, 0))
        actual_action_score = find_minimax_action((self.action1, 2), (action_col, 2), ge)
        self.assertEqual(actual_action_score, (self.action1, 2))
        
    def test_find_minimax_action_le(self):
        action_score = find_minimax_action((self.action1, 8), (self.action2, 1), le)
        self.assertEqual(action_score, (self.action2, 1))

    def test_place_penguin_across_full_state(self):
        posn = (0,0)
        self.assertTrue(self.state_full.is_tile_available(posn))
        new_state = place_penguin_across(self.state_full, Color.RED)
        self.assertFalse(new_state.is_tile_available(posn))
        self.assertEqual(new_state.get_player(Color.RED).get_penguins(), [posn])

    def test_place_penguin_across_holes(self):
        posn = (1,0)
        self.assertTrue(self.state_holes.is_tile_available(posn))
        new_state = place_penguin_across(self.state_holes, Color.RED)
        self.assertFalse(new_state.is_tile_available(posn))
        self.assertEqual(new_state.get_player(Color.RED).get_penguins(), [posn])
    
    def test_place_penguin_across_other_penguin(self):
        new_state = place_penguin_across(self.state_full, Color.RED)
        next_penguin = (0, 1)
        self.assertTrue(new_state.is_tile_available(next_penguin))
        next_state = place_penguin_across(new_state, Color.WHITE)
        self.assertFalse(next_state.is_tile_available(next_penguin))
        self.assertEqual(next_state.get_player(Color.WHITE).get_penguins(), [next_penguin])

    """
    def test_choose_action_minimax_1_turn(self):
        self.player1.add_penguin((0,0))
        self.assertEqual(choose_action_minimax(self.game_tree, 1), Move((0,0), (1,0)))
    """
    def test_choose_action_minimax_2_turn(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((3,0)) # will minimize player1's moves will go to 2, 1
        self.assertEqual(choose_action_minimax(self.game_tree,3), Move((0,0), (1,0)))
    
    """
    def test_choose_action_minimax_subtree_base_no_moves(self):
        board = Board(2, 2)
        board_array = [
            [1, 2],
            [0, 1]
        ]
        board.create_board_from_json(board_array)
        state = State(self.players, board)
        self.player1.add_penguin((0, 0))
    """


    