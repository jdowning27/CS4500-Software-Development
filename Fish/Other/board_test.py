import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)
import unittest
from unittest import mock
import random
from board import *
from tile import *
from skip import Skip

class BoardTestCase(unittest.TestCase):

    def setUp(self):
        self.board = Board(4, 3)
        self.board.create_board_without_holes(4)

    def test_make_board_with_neg_row(self):
        self.assertRaisesRegex(ValueError, "row and col must be positive", Board, -1, 5)
    
    def test_make_board_with_neg_col(self):
        self.assertRaisesRegex(ValueError, "row and col must be positive", Board, 5, -1)
    
    def test_make_board_with_zeros(self):
        self.assertRaisesRegex(ValueError, "row and col must be positive", Board, 0, 0)

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
        self.assertRaisesRegex(ValueError, "fish must be positive and less than the max allowed fish",
            board.create_board_without_holes, 0)

    def test_create_board_json(self):
        tiles = [
            [1,     2,      3,      0],
                [4,     0,      0,      5],
            [1,     1,      0,      1]
        ]
        board = Board(3, 4)
        board.create_board_from_json(tiles)
        for r in range(0, len(tiles)):
            for c in range(0, len(tiles[r])):
                self.assertEqual(board.tiles[c][r].fish, tiles[r][c])

    def test_create_board_json_short_row(self):
        tiles = [
            [1,     2],    
                [4,     0,      0,      5],
            [1,     1,      0,      1]
        ]
        board = Board(3, 4)
        board.create_board_from_json(tiles)
        self.assertEqual(board.tiles[2][0].fish, 0)
        self.assertEqual(board.tiles[3][0].fish, 0)
        self.assertFalse(board.tiles[2][0].is_active)
        self.assertFalse(board.tiles[3][0].is_active)
    

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
    
    def test_create_board_negative_one_fish(self):
        self.assertRaisesRegex(ValueError, "the number of tiles with one fish cannot be negative", 
            self.board.create_board_with_holes, [(0,0), (0,1)], -2)

    def test_create_board_too_many_holes(self):
        self.assertRaisesRegex(ValueError, "holes and number of one fish tiles cannot be greater than the total number of tiles", 
            self.board.create_board_with_holes, [(0,0), (0,1)], 12)

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

    def test_get_reachable_posn_se(self):
        board = Board(3, 3)
        board.create_board_without_holes(3)
        self.assertEqual(board.get_reachable_posn_dir(0, 0, Tile.get_se_coord), [(1, 0), (2, 1)])
        self.assertEqual(board.get_reachable_posn_dir(1, 0, Tile.get_se_coord), [(2, 1)])

    def test_get_reachable_posn_sw(self):
        board = Board(3, 3)
        board.create_board_without_holes(3)
        self.assertEqual(board.get_reachable_posn_dir(0, 0, Tile.get_sw_coord), [])
        self.assertEqual(board.get_reachable_posn_dir(1, 0, Tile.get_sw_coord), [(2, 0)])

    def test_get_all_reachable_posn(self):
        board = Board(4, 3)
        board.create_board_without_holes(1)
        self.assertEqual(board.get_all_reachable_posn(0,0), [(2, 0), (1, 0), (2, 1), (3, 1)])

    def test_get_all_reachable_posn_holes(self):
        board = Board(4, 3)
        board.create_board_with_holes([(0,0)], 1)
        self.assertEqual(board.get_all_reachable_posn(1, 0), [(3, 0), (0, 1), (2, 0), (2, 1), (3, 1)])

    def test_tile_exists(self):
        board = Board(3, 3)
        self.assertTrue(board.tile_exists((2,2)))
        self.assertFalse(board.tile_exists((-1, 1)))
        self.assertFalse(board.tile_exists((3, 1)))

    def test_get_coordinates_from_num(self):
        board = Board(3, 3)
        self.assertEqual(board.get_coordinates_from_num(5), (2, 1))
        self.assertEqual(board.get_coordinates_from_num(6), (0, 2))
        self.assertEqual(board.get_coordinates_from_num(7), (1, 2))

    def test_set_all(self):
        board = Board(3, 3)
        for col in board.tiles:
            for t in col:
                self.assertEqual(t.fish, None)
        board.set_all(3)
        for col in board.tiles:
            for t in col:
                self.assertEqual(t.fish, 3)

    def test_remove_tile(self):
        board = Board(3, 3)
        self.assertTrue(board.tiles[0][0].is_active)
        board.remove_tile(0, 0)
        self.assertFalse(board.tiles[0][0].is_active)

    @mock.patch('random.sample')
    @mock.patch('random.random')
    def test_set_random_tile(self, random, random_set):
        random_set.return_value = [5, 7]
        random.return_value = .4
        board = Board(3, 3)
        board.create_board_without_holes(3)
        for col in board.tiles:
            for t in col:
                self.assertEqual(t.fish, 3)
        board.set_random_tiles(2)
        self.assertEqual(board.tiles[1][2].fish, 2)
        self.assertEqual(board.tiles[2][1].fish, 2)

    def test_get_offset(self):
        size = GUI_UNIT * MAX_FISH
        board = Board(4, 3)
        self.assertEqual(board.get_offset(0,0), (0, 0))
        tile2_off_x = 16 * size 
        tile2_off_y = size * 4
        self.assertEqual(board.get_offset(4, 4), (tile2_off_x, tile2_off_y))
        tile3_off_x = 12 * size + (2 * size)
        tile3_off_y = size * 3
        self.assertEqual(board.get_offset(3, 3), (tile3_off_x, tile3_off_y))

    def test_board_get_reachable_penguins(self):
        positions = self.board.get_all_reachable_posn(0, 0, [(2, 1)])
        self.assertEqual(positions, [(2,0), (1,0)])

