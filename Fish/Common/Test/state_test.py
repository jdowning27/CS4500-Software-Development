import unittest
from unittest.mock import MagicMock
from State import *
from Board import *
from Player import *
from Color import *


class StateTestCase(unittest.TestCase):

    def setUp(self):
        self.board_full = Board(4, 3)
        self.board_full.create_board_without_holes(4)
        self.board_holes = Board(4, 3)
        self.board_holes.create_board_with_holes([(0,0), (1,1)], 3)

        self.player1 = Player(Color.RED, 5)
        self.player2 = Player(Color.WHITE, 10)
        self.players = [self.player1, self.player2]

        self.state_full = State(self.players, self.board_full)
        self.state_holes = State(self.players, self.board_holes)

    def test_place_penguin_for_player_success(self):
        self.assertEqual(self.state_full.get_all_penguins(), [])
        self.state_full.place_penguin_for_player(Color.RED, (1, 2))
        self.assertEqual(self.state_full.get_all_penguins(), [(1, 2)])

    def test_place_penguin_for_player_out_of_bounds(self):
        self.assertEqual(self.state_full.get_all_penguins(), [])
        self.state_full.place_penguin_for_player(Color.RED, (4, 3))
        self.assertEqual(self.state_full.get_all_penguins(), [])
    
    def test_place_penguin_for_player_hole(self):
        self.assertEqual(self.state_holes.get_all_penguins(), [])
        self.state_holes.place_penguin_for_player(Color.RED, (0, 0))
        self.assertEqual(self.state_holes.get_all_penguins(), [])
    
    def test_place_penguin_for_player_no_player(self):
        self.assertEqual(self.state_full.get_all_penguins(), [])
        self.state_full.place_penguin_for_player(Color.BROWN, (1, 2))
        self.assertEqual(self.state_full.get_all_penguins(), [])

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
        self.state_full.place_penguin_for_player(Color.RED, (1, 2))
        self.assertFalse(self.state_full.is_tile_available((1, 2)))
    
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

        self.state_full.move_penguin((0, 0), (2, 0))
        self.assertTrue((2, 0) in self.state_full.get_all_penguins())
        self.assertFalse((0, 0) in self.state_full.get_all_penguins())

    def test_move_penguin_occupied(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((2,0))
        self.assertEqual(self.state_full.get_all_penguins(), [(0, 0), (2, 0)])
        self.state_full.move_penguin((0, 0), (2, 0))
        self.assertEqual(self.state_full.get_all_penguins(), [(0, 0), (2, 0)])
        # check that the penguins for each player did not trade places
        self.assertEqual(self.player1.get_penguins(), [(0,0)])
        self.assertEqual(self.player2.get_penguins(), [(2,0)])

    def test_any_remaining_moves_true(self):
        self.player1.add_penguin((0,0))
        self.player2.add_penguin((2,0))
        self.assertTrue(self.state_full.any_remaining_moves())

    def test_any_remaining_moves_no_penguins(self):
        self.assertFalse(self.state_full.any_remaining_moves())

    def test_any_remaining_moves_no_moves(self):
        board = Board(4, 3)
        board.create_board_with_holes([(1, 0), (2, 0)], 0)
        state = State([self.player1], board)
        self.player1.add_penguin((0,0))
        self.assertFalse(state.any_remaining_moves())
