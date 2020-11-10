import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

import unittest
from game_tree import GameTree
from state import *
from board import *
from Player import *
from color import *
from move import *


class GameTreeTestCase(unittest.TestCase):

    def setUp(self):
        self.board_full = Board(4, 3)
        self.board_full.create_board_without_holes(4)
        self.board_holes = Board(4, 3)
        self.board_holes.create_board_with_holes([(1, 0), (2,0)], 3)

        self.player1 = Player(Color.RED, 5)
        self.player2 = Player(Color.WHITE, 10)
        self.players = [self.player1, self.player2]

        self.state_full = State(self.players, self.board_full)
        self.state_holes = State(self.players, self.board_holes)

        self.player1.add_penguin((0,0))
        self.player2.add_penguin((0,2))

        self.action1 = Move((0,0), (1,0))

        self.game_tree = GameTree(self.state_full)
        self.game_tree_holes = GameTree(self.state_holes)

        self.state1_0 = self.state_full.move_penguin((0,0), (1,0))
        self.state2_0 = self.state_full.move_penguin((0,0), (2,0))
        self.state2_1 = self.state_full.move_penguin((0,0), (2,1))
        self.state3_1 = self.state_full.move_penguin((0,0), (3,1))


    def test_attempt_move(self):
        self.assertEqual(type(self.game_tree.attempt_move(self.action1)), GameTree)

    def test_attempt_move_invalid(self):
        self.assertFalse(self.game_tree.attempt_move(Move((0,0), (2,2))))

    def test_get_child_trees(self):
        states = [self.state1_0, self.state2_0, self.state2_1, self.state3_1]
        child_trees = GameTree.get_child_trees(self.game_tree)
        for state in states:
            self.assertTrue(GameTree(state) in child_trees)
        self.assertEqual(len(child_trees), len(states))

    def test_get_child_trees_no_moves(self):
        child_trees = GameTree.get_child_trees(self.game_tree_holes)
        self.assertEqual(len(child_trees), 1)
        self.state_holes.set_next_players_turn()
        self.assertTrue(child_trees[0] in [GameTree(self.state_holes)])

    def test_get_child_trees_player2(self):
        self.game_tree_holes.state.set_next_players_turn()
        self.assertEqual(len(GameTree.get_child_trees(self.game_tree_holes)), 5)

    def test_create_child_trees(self):
        trees = [GameTree(self.state1_0), GameTree(self.state2_0), GameTree(self.state2_1), GameTree(self.state3_1)]
        children = self.game_tree.create_child_trees()
        for tree in trees:
            self.assertTrue(tree in children.values())
        self.assertEqual(len(children), len(trees))

    def test_create_child_trees_no_children(self):
        children = self.game_tree_holes.create_child_trees()
        child_trees = list(children.values())
        self.assertEqual(len(child_trees), 1)
        self.state_holes.set_next_players_turn()
        self.assertTrue(child_trees[0] in [GameTree(self.state_holes)])

    def test_apply_to_children(self):
        action = Move((0,2), (1,2))
        states = [self.state1_0, self.state2_0, self.state2_1, self.state3_1]
        new_states = self.game_tree.apply_to_children(action.apply_move)
        for state in states:
            move_state = state.move_penguin((0,2), (1,2))
            self.assertTrue(move_state in new_states)
        self.assertEqual(len(new_states), len(states))

    def test_apply_to_children_get_children(self):
        child_trees = self.game_tree.apply_to_children(GameTree.get_child_trees)
        self.assertEqual(len(child_trees), 4)
        num_children = 0
        for c in child_trees:
            num_children += len(c)
            self.assertGreater(len(c), 0)
        self.assertEqual(num_children, 18)
            

    def test_apply_to_children_create_trees(self):
        child_trees = self.game_tree.apply_to_children(GameTree.create_child_trees)
        self.assertEqual(len(child_trees), 4)
        num_children = 0
        for c in child_trees:
            num_children += len(c)
            self.assertGreater(len(c), 0)
        self.assertEqual(num_children, 18)

    def test_create_n_layers_tree(self):
        board_array = [
            [1,     2],
                [1,     2],
            [1,     2]
        ]
        board = Board(3, 2)
        board.create_board_from_json(board_array)
        p1 = Player(Color.RED, 5)
        p2 = Player(Color.WHITE, 5)
        players = [p1, p2]
        p1.add_penguin((0,0))
        state = State(players, board)

        game_tree = GameTree(state)
        game_tree.create_n_layers_tree(5)
        json_tree = game_tree.print_children()
        self.assertEqual(len(json_tree), 3) #p1 has 3 possible moves
        self.assertEqual(len(json_tree[0][1]), 1) #p2 has no penguins => no moves


