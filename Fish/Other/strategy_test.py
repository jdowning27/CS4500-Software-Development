import unittest
from operator import le, ge

from Fish.Player.strategy import *
from Fish.Common.game_tree import *
from Fish.Common.state import *
from Fish.Common.board import *
from Fish.Common.player_data import PlayerData
from Fish.Common.color import *
from Fish.Common.move import *


class StrategyTestCase(unittest.TestCase):

    def setUp(self):
        self.strategy = Strategy()
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
        mini_board_array = [
            [1,     5],
                [2,     10],
            [7,     5]
        ]
        self.mini_board = Board(3, 2)
        self.mini_board.create_board_from_json(mini_board_array)

        self.player1 = PlayerData(Color.RED, 5)
        self.player2 = PlayerData(Color.WHITE, 10)
        self.players = [self.player1, self.player2]

        self.state_full = State(self.players, self.board_full)
        self.state_holes = State(self.players, self.board_holes)
        self.mini_state = State(self.players, self.mini_board)
        self.mini_tree = GameTree(self.mini_state)

        self.action1 = Move((0,0), (1,0))
        self.action2 = Move((2,0), (3,0))

        self.game_tree = GameTree(self.state_full)
        self.game_tree_holes = GameTree(self.state_holes)

        self.state1_0 = self.state_full.move_penguin((0,0), (1,0))
        self.state2_0 = self.state_full.move_penguin((0,0), (2,0))
        self.state2_1 = self.state_full.move_penguin((0,0), (2,1))
        self.state3_1 = self.state_full.move_penguin((0,0), (3,1))

    def test_find_minimax_action_score(self):
        action_score = self.strategy.find_minimax_action((self.action1, 8), (self.action2, 1), ge)
        self.assertEqual(action_score, (self.action1, 8))

    def test_find_minimax_action_row_ge(self):
        action_row = Move((1, 0), (1, 0))
        actual_action_score = self.strategy.find_minimax_action((self.action1, 2), (action_row, 2), ge)
        self.assertEqual(actual_action_score, (self.action1, 2))

    def test_find_minimax_action_col_ge(self):
        action_col = Move((3,0), (1, 0))
        actual_action_score = self.strategy.find_minimax_action((self.action1, 2), (action_col, 2), ge)
        self.assertEqual(actual_action_score, (self.action1, 2))
        
    def test_find_minimax_action_le(self):
        action_score = self.strategy.find_minimax_action((self.action1, 8), (self.action2, 1), le)
        self.assertEqual(action_score, (self.action2, 1))

    def test_place_penguin_across_full_state(self):
        posn = (0,0)
        self.assertTrue(self.state_full.is_tile_available(posn))
        self.assertEqual(self.strategy.place_penguin_across(self.state_full), posn)

    def test_place_penguin_across_holes(self):
        posn = (1,0)
        self.assertTrue(self.state_holes.is_tile_available(posn))
        self.assertEqual(self.strategy.place_penguin_across(self.state_holes), posn)
    
    def test_place_penguin_across_other_penguin(self):
        new_state = self.state_full.place_penguin_for_player(Color.RED, (0,0))
        next_penguin = (0, 1)
        self.assertTrue(new_state.is_tile_available(next_penguin))
        self.assertEqual(self.strategy.place_penguin_across(new_state), next_penguin)
    def test_place_penguin_across_no_spaces(self):
        state = self.mini_state.place_penguin_for_player(Color.RED, (0, 0))
        state = state.place_penguin_for_player(Color.WHITE, (0, 1))
        state = state.place_penguin_for_player(Color.RED, (1, 0))
        state = state.place_penguin_for_player(Color.WHITE, (1, 1))
        state = state.place_penguin_for_player(Color.RED, (2, 0))
        state = state.place_penguin_for_player(Color.WHITE, (2, 1))
        self.assertTrue(self.strategy.place_penguin_across(state) is False)

    def test_choose_action_minimax_1_turn(self):
        self.player1.add_penguin((0,0))
        self.assertEqual(self.strategy.choose_action_minimax(self.game_tree, 1).print_json(), [(0,0), (1,0)])

    def test_choose_action_minimax_1_turn_other_penguins(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((2,1))
        action = self.strategy.choose_action_minimax(self.mini_tree, 2)
        self.assertEqual(action.print_json(), [(0,0), (1, 0)])
    
    def test_choose_action_minimax_2_turn(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((3,0)) 
        self.assertEqual(self.strategy.choose_action_minimax(self.game_tree, 2).print_json(), [(0,0), (1,0)])

    def test_choose_action_minimax_little_tree(self):
        self.player1.add_penguin((0,0))
        action = self.strategy.choose_action_minimax(self.mini_tree, 2)
        self.assertEqual(action.print_json(), [(0,0), (2, 0)])
        action1 = self.strategy.choose_action_minimax(self.mini_tree, 3)
        self.assertEqual(action1.print_json(), [(0,0), (2, 1)])

    def test_choose_action_minimax_no_moves(self):
        self.player1.add_penguin((1, 0))
        self.player2.add_penguin((2, 0))
        self.player2.add_penguin((3, 0))
        self.player2.add_penguin((2, 1))
        action = self.strategy.choose_action_minimax(self.game_tree_holes, 3)
        self.assertEqual(action.print_json(), False)

    def test_choose_action_minimax_more_layers(self):
        self.player1.add_penguin((1, 0))
        action = self.strategy.choose_action_minimax(self.mini_tree, 10)
        self.assertEqual(action.print_json(), [(1, 0), (0, 1)])
        self.assertNotEqual(action.print_json(), False)

    def test_choose_action_minimax_subtree(self):
        self.player1.add_penguin((0, 0))
        action = self.strategy.choose_action_minimax_subtree(self.game_tree, 6, Color.RED)
        self.assertEqual(action[0].print_json(), [(0, 0), (1, 0)])


    
