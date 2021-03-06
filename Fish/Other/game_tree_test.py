import unittest
from Fish.Common.game_tree import GameTree
from Fish.Common.game_ended import GameEnded
from Fish.Common.state import *
from Fish.Common.board import *
from Fish.Common.player_data import PlayerData
from Fish.Common.color import *
from Fish.Common.move import *


class GameTreeTestCase(unittest.TestCase):

    def setUp(self):
        self.board_full = Board(4, 3)
        self.board_full.create_board_without_holes(4)
        self.board_holes = Board(4, 3)
        self.board_holes.create_board_with_holes([(1, 0), (2,0)], 3)

        self.player1 = PlayerData(Color.RED, 5)
        self.player2 = PlayerData(Color.WHITE, 10)
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
    
    def test_attempt_move_last_move(self):
        mini_board_array = [
            [1,     5],
                [2,     1],
            [1,     5],
                [1,     5],
            [0,     5]
        ]
        player1 = PlayerData(Color.RED)
        player2 = PlayerData(Color.WHITE)
        player1.add_penguin((0,0))
        player1.add_penguin((1,0))
        player1.add_penguin((2,0))
        player1.add_penguin((3,0))
        player2.add_penguin((0,1))
        player2.add_penguin((1,1))
        player2.add_penguin((2,1))
        player2.add_penguin((3,1))
        players = [player1, player2]
        board = Board(5, 2)
        board.create_board_from_json(mini_board_array)
        state = State(players, board)
        game_tree = GameTree(state)
        action = Move((3, 0), (4, 1))
        self.assertEqual(type(game_tree.attempt_move(action)), GameEnded)

    def test_attempt_move_invalid(self):
        self.assertFalse(self.game_tree.attempt_move(Move((0,0), (2,2))))

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

    def test_apply_to_children_create_trees(self):
        child_trees = self.game_tree.apply_to_children(GameTree.create_child_trees)
        self.assertEqual(len(child_trees), 4)
        num_children = 0
        for c in child_trees:
            num_children += len(c)
            self.assertGreater(len(c), 0)
        self.assertEqual(num_children, 18)
