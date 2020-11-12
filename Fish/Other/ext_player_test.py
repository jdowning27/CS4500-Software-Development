import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Player'
sys.path.append(os_path)

import unittest
from player import Player
from player_data import PlayerData
from board import Board
from color import Color
from state import State
from game_tree import GameTree
from strategy import Strategy

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player1 = Player()
        self.player2 = Player()
        mini_board_array = [
            [1,     5],
                [2,     1],
            [1,     5]
        ]
        self.mini_board = Board(3, 2)
        self.mini_board.create_board_from_json(mini_board_array)
        self.strategy = Strategy()
        self.in_player1 = PlayerData(Color.RED)
        self.in_player2 = PlayerData(Color.WHITE)
        self.players = [self.in_player1, self.in_player2]
        self.mini_state = State(self.players, self.mini_board)
        self.mini_tree = GameTree(self.mini_state)

    def test_choose_placement(self):
        self.assertEqual(self.player1.choose_placement(self.mini_state), (0, 0))
        next_state = self.mini_state.place_penguin_for_player(Color.RED, (0, 0))
        self.assertEqual(self.player1.choose_placement(next_state), (0, 1))

    def test_choose_placement_wrap(self):
        next_state = self.mini_state.place_penguin_for_player(Color.RED, (0, 0))
        next_state = next_state.place_penguin_for_player(Color.RED, (0, 1))
        self.assertEqual(self.player1.choose_placement(next_state), (1, 0))

    def test_choose_next_move(self):
        next_state = self.mini_state.place_penguin_for_player(Color.RED, (0, 0))
        next_state = next_state.place_penguin_for_player(Color.WHITE, (0, 1))
        self.player1.set_state(next_state)
        self.assertEqual(self.player1.choose_next_move().print_json(), [(0,0), (2, 1)])

    def test_choose_next_move_no_moves(self):
        next_state = self.mini_state.place_penguin_for_player(Color.RED, (0, 0))
        next_state = next_state.place_penguin_for_player(Color.WHITE, (1, 0))
        next_state = next_state.place_penguin_for_player(Color.WHITE, (2, 0))
        self.player1.set_state(next_state)
        self.assertEqual(self.player1.choose_next_move().print_json(), "Skip")

    def test_assign_color(self):
        self.assertEqual(self.player1.get_color(), None)
        self.player1.assign_color(Color.RED)
        self.assertEqual(self.player1.get_color(), Color.RED)

    def test_assign_color_twice(self):
        self.assertEqual(self.player1.get_color(), None)
        self.player1.assign_color(Color.RED)
        self.assertEqual(self.player1.get_color(), Color.RED)
        self.player1.assign_color(Color.WHITE)
        self.assertEqual(self.player1.get_color(), Color.WHITE)
