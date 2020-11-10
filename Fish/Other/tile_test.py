import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

import unittest
from tile import *
from constants import MAX_FISH, GUI_UNIT


class TileTestCase(unittest.TestCase):
    def test_create_hole(self):
        tile = Tile(0, 0)
        tile.set_fish(3)
        self.assertTrue(tile.is_active)
        self.assertGreater(tile.fish, 0)
        tile.create_hole()
        self.assertFalse(tile.is_active)
        self.assertEqual(tile.fish, 0)

    def test_set_fish(self):
        num_fish = 3
        tile = Tile(4, 3)
        self.assertEqual(tile.fish, None)
        tile.set_fish(num_fish)
        self.assertEqual(tile.fish, num_fish)

    def test_get_north_coord(self):
        tile = Tile(0, 0)
        self.assertEqual(tile.get_north_coord(), (-2, 0))
        tile2 = Tile(4, 3)
        self.assertEqual(tile2.get_north_coord(), (2, 3))

    def test_get_south_coord(self):
        tile = Tile(0, 0)
        self.assertEqual(tile.get_south_coord(), (2, 0))
        tile2 = Tile(4, 3)
        self.assertEqual(tile2.get_south_coord(), (6, 3))

    def test_get_ne_coord(self):
        tile = Tile(2, 4)
        self.assertEqual(tile.get_ne_coord(), (1, 4))
        tile2 = Tile(3, 3)
        self.assertEqual(tile2.get_ne_coord(), (2, 4))

    def test_get_nw_coord(self):
        tile = Tile(2, 4)
        self.assertEqual(tile.get_nw_coord(), (1, 3))
        tile2 = Tile(3, 3)
        self.assertEqual(tile2.get_nw_coord(), (2, 3))

    def test_get_se_coord(self):
        tile = Tile(2, 4)
        self.assertEqual(tile.get_se_coord(), (3, 4))
        tile2 = Tile(3, 3)
        self.assertEqual(tile2.get_se_coord(), (4, 4))

    def test_get_sw_coord(self):
        tile = Tile(2, 4)
        self.assertEqual(tile.get_sw_coord(), (3, 3))
        tile2 = Tile(3, 3)
        self.assertEqual(tile2.get_sw_coord(), (4, 3))

    def test_get_hex_points(self):
        tile = Tile(0, 0)
        self.assertEqual(tile.get_hex_points((0, 0)), [
                         100, 0, 200, 0, 300, 100, 200, 200, 100, 200, 0, 100])
        tile2 = Tile(1, 2)
        self.assertEqual(tile2.get_hex_points((100, 100)), [
                         200, 100, 300, 100, 400, 200, 300, 300, 200, 300, 100, 200])

