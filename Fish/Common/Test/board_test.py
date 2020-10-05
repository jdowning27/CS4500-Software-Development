import unittest
import Board
from Board import *
import Tile
from Tile import *

class BoardTestCase(unittest.TestCase):
    def test_create_board_with_holes(self):
        board = Board(4, 2)
        holes = [(0,0), (1,1)]
        min_tiles = 1
        board.create_board_with_holes(holes, min_tiles)
        num_1_tiles = 0
        for c in range(0, board.col):
            for r in range(0, board.row):
                if board.tiles[c][r].fish == 1:
                    num_1_tiles += 1
        self.assertGreaterEqual(num_1_tiles, min_tiles)
        self.assertFalse(board.tiles[0][0].is_active)
        self.assertFalse(board.tiles[1][1].is_active)

    def test_create_board_without_holes(self):
        board = Board(2, 2)
        num_fish = 4
        board.create_board_without_holes(num_fish)
        for c in range(0, board.col):
            for r in range(0, board.row):
                self.assertEqual(board.tiles[c][r].fish, num_fish)
    
    def test_create_board_without_holes_error(self):
        board = Board(2, 2)
        with self.assertRaises(SystemExit) as err:
            board.create_board_without_holes(0)
        self.assertEqual(err.exception.code, 1)

    def test_remove_tile(self):
        board = Board(2, 2)
        num_fish = 3
        row, col = [1, 1]
        board.create_board_without_holes(num_fish)
        tile = board.tiles[col][row]
        self.assertTrue(tile.is_active)
        self.assertEqual(tile.fish, num_fish)
        board.remove_tile(row, col)
        self.assertEqual(tile.fish, 0)
        self.assertFalse(tile.is_active)

    def test_tile_exists(self):
        board = Board(2, 2)
        holes = [(0,0)]
        board.create_board_with_holes(holes, 1)
        self.assertTrue(board.tile_exists((0,1)))
        self.assertFalse(board.tile_exists((0,0)))
        self.assertFalse(board.tile_exists((0,5)))

    def test_get_reachable_posn_north(self):
        board = Board(8, 1)
        board.create_board_without_holes(3)
        self.assertEqual(board.get_reachable_posn_dir(7, 0, Tile.get_north_coord), [(5, 0), (3, 0), (1, 0)])
        self.assertEqual(board.get_reachable_posn_dir(0, 0, Tile.get_north_coord), [])

    def test_get_reachable_posn_south(self):
        board = Board(8, 1)
        board.create_board_without_holes(3)
        self.assertEqual(board.get_reachable_posn_dir(7, 0, Tile.get_south_coord), [])
        self.assertEqual(board.get_reachable_posn_dir(1, 0, Tile.get_south_coord), [(3, 0), (5, 0), (7, 0)])

    def test_get_reachable_posn_ne(self):
        board = Board(3, 3)
        board.create_board_without_holes(3)
        self.assertEqual(board.get_reachable_posn_dir(0, 0, Tile.get_ne_coord), [])
        self.assertEqual(board.get_reachable_posn_dir(1, 0, Tile.get_ne_coord), [(0, 1)])

    def test_get_reachable_posn_nw(self):
        board = Board(3, 3)
        board.create_board_without_holes(3)
        self.assertEqual(board.get_reachable_posn_dir(0, 0, Tile.get_nw_coord), [])
        self.assertEqual(board.get_reachable_posn_dir(1, 0, Tile.get_nw_coord), [(0, 0)])

    def test_get_all_reachable_posn(self):
        board = Board(4, 3)
        board.create_board_without_holes(1)
        self.assertEqual(board.get_all_reachable_posn(0,0), [(2, 0), (1, 0), (2, 1), (3, 1)])
    
    def test_get_all_reachable_posn_holes(self):
        board = Board(4, 3)
        board.create_board_with_holes([(0,0)], 1)
        self.assertEqual(board.get_all_reachable_posn(1, 0), [(3, 0), (0, 1), (2, 0), (2, 1), (3, 1)])


    


        
