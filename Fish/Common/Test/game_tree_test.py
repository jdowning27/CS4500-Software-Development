import unittest
from game_tree import *
from State import *
from Board import *
from Player import *
from Color import *
from Action import *


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

        self.action1 = Action((0,0), (1,0))

        self.game_tree = GameTree(self.state_full)

        self.state1_0 = self.state_full.move_penguin((0,0), (1,0))
        self.state2_0 = self.state_full.move_penguin((0,0), (2,0))
        self.state2_1 = self.state_full.move_penguin((0,0), (2,1))
        self.state3_1 = self.state_full.move_penguin((0,0), (3,1))


    def test_attempt_move(self):
        self.assertEqual(type(self.game_tree.attempt_move(self.state_full, self.action1)), State)

    def test_attempt_move_false(self):
        self.assertFalse(self.game_tree.attempt_move(self.state_full, Action((0,0), (2,2))))

    def test_get_child_states(self):
        states = [self.state1_0, self.state2_0, self.state2_1, self.state3_1]
        child_states = self.game_tree.get_child_states(self.state_full)
        for state in states:
            self.assertTrue(state in child_states)
        self.assertEqual(len(child_states), len(states))

    def test_create_child_trees(self):
        trees = [GameTree(self.state1_0), GameTree(self.state2_0), GameTree(self.state2_1), GameTree(self.state3_1)]
        children = self.game_tree.create_child_trees()
        for tree in trees:
            self.assertTrue(tree in children.values())
        self.assertEqual(len(children), len(trees))

    def test_create_child_trees_no_children(self):
        game_tree_holes = GameTree(self.state_holes)
        children = game_tree_holes.create_child_trees()
        self.assertEqual(children, {})
        self.assertEqual(len(children), 0)

    def test_apply_to_children(self):
        action = Action((0,2), (1,2))
        states = [self.state1_0, self.state2_0, self.state2_1, self.state3_1]
        new_states = self.game_tree.apply_to_children(self.state_full, action.apply_move)
        for state in states:
            move_state = state.move_penguin((0,2), (1,2))
            self.assertTrue(move_state in new_states)
        self.assertEqual(len(new_states), len(states))
