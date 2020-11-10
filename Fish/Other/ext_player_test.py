import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Player'
sys.path.append(os_path)

import unittest
from player import Player as ExtPlayer
from Player import Player as IntPlayer
from board import Board
from color import Color
from state import State
from game_tree import GameTree
from strategy import Strategy

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player1 = ExtPlayer()
        self.player2 = ExtPlayer()
        mini_board_array = [
            [1,     5],
                [2,     10],
            [7,     5]
        ]
        self.mini_board = Board(3, 2)
        self.mini_board.create_board_from_json(mini_board_array)
        self.strategy = Strategy()
        self.in_player1 = IntPlayer(Color.RED)
        self.in_player2 = IntPlayer(Color.WHITE)
        self.players = [self.in_player1, self.in_player2]
        self.mini_state = State(self.players, self.mini_board)
        self.mini_tree = GameTree(self.mini_state)


    def test_choose_next_move(self):
        self.assertEqual(self.player1.choose_next_move(self.mini_tree), self.strategy.choose_action_minimax(self.mini_tree, 3))

    def test_place_penguin(self):
        self.assertEqual(self.player1.place_penguin(self.mini_state), self.strategy.place_penguin_across(self.mini_state))
        self.assertEqual(self.player1.get_penguins(), {(0,0)})

    def test_assign_color(self):
        self.assertEqual(self.player1.get_color(), None)
        self.player1.assign_color(Color.RED)
        self.assertEqual(self.player1.get_color(), Color.RED)

    def test_cant_double_assign_color(self):
        self.player1.assign_color(Color.RED)
        self.assertEqual(self.player1.get_color(), Color.RED)
        self.player1.assign_color(Color.WHITE)
        self.assertEqual(self.player1.get_color(), Color.RED)

    def test_move_penguin(self):
        self.player1.place_penguin(self.mini_state)
        self.assertEqual(self.player1.get_penguins(), {(0, 0)})
        self.assertEqual(self.player1.get_fish(), 0)
        self.player1.move_penguin((0,0), (1,0), 1)
        self.assertEqual(self.player1.get_penguins(), {(1, 0)})
        self.assertEqual(self.player1.get_fish(), 1)

    def test_remove_penguins(self):
        self.player1.place_penguin(self.mini_state)
        self.assertEqual(self.player1.get_penguins(), {(0, 0)})
        self.player1.remove_penguins()
        self.assertEqual(self.player1.get_penguins(), None)

