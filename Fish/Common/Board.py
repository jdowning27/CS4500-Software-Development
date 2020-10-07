import math
import random
import sys
from tkinter import *

from Tile import *
from Util import validate_non_neg_int, validate_pos_int, print_error
import Constants

master = Tk()

class Board:

    def __init__(self, row, col):
        """
        Constructor that initializes the game board of size Row by Col

        :row: int       The number of rows
        :col: int       The number of columns
        """
        self.tiles = [[None for r in range(0, row)] for c in range(0, col)]
        self.col = col
        self.row = row

    def init_board(self):
        """
        Intializes the game board with Tile objects in each place
        """
        for c in range(0, self.col):
            for r in range(0, self.row):
                self.tiles[c][r] = Tile(r, c)

    def create_board_with_holes(self, holes, min):
        """
        Create board with given holes and min number of tiles with 1 Fish

        :holes: array         List of (x, y) positions where there are holes in board
        :min:   int           The minimum number of tiles with one fish
        """
        self.init_board()
        validate_non_neg_int(len(holes), min)
        if len(holes) + min > (self.row * self.col):
            print_error(
                "usage: Invalid Input: holes + min > Total number of tiles")
        self.set_all(1)
        self.print_board()
        for h in holes:
            r, c = h
            self.remove_tile(r, c)
        self.print_board()
        self.set_random_tiles(self.col * self.row - (len(holes) + min))
        self.print_board()

    def create_board_without_holes(self, fish):
        """
        Create board with no holes, and set all tiles to have a specific
        number of fish.

        :fish: int          The number of fish per tile
        """
        self.init_board()
        validate_pos_int(fish)
        self.set_all(fish)

    def get_all_reachable_posn(self, row, col):
        """
        Get all reachable board positions from (row, col)

        :returns: array     List of (row, col) representing all possible reachable positions
        """
        result = []
        # get reachable positions in every direction
        result.extend(self.get_reachable_posn_dir(
            row, col, Tile.get_north_coord))
        result.extend(self.get_reachable_posn_dir(
            row, col, Tile.get_south_coord))
        result.extend(self.get_reachable_posn_dir(row, col, Tile.get_nw_coord))
        result.extend(self.get_reachable_posn_dir(row, col, Tile.get_ne_coord))
        result.extend(self.get_reachable_posn_dir(row, col, Tile.get_sw_coord))
        result.extend(self.get_reachable_posn_dir(row, col, Tile.get_se_coord))
        return result

    def get_reachable_posn_dir(self, row, col, get_dir_coord):
        """
        Get all reachable positions on board from give (row, col) Tile.
        Result is a list of (row, col)

        :row: int               Current tile's row
        :col: int               Current tile's column
        :get_dir_coord: func    Function to get the next tile in specific direction
        :returns: array         List of (row, col) reachable tiles to the give direction
        """
        next_tile = get_dir_coord(self.tiles[col][row])
        if self.tile_exists(next_tile):
            result = [next_tile]
            result.extend(self.get_reachable_posn_dir(
                next_tile[0], next_tile[1], get_dir_coord))
            return result
        else:
            return []

    def tile_exists(self, tile_coords):
        """
        Is the tile in bounds and active?

        :tile_coords: tuple     The tile's coordinates to check
        :returns: bool          True if the tile is within game board dimensions, and is active
        """
        row, col = tile_coords
        return row >= 0 and row < self.row and col >= 0 and col < self.col and self.tiles[col][row].is_active

    def set_random_tiles(self, num_set):
        """
        Randomly assign fish values to given number of tiles on the board.

        :num_set: int       The number of tiles to randomly set
        """
        rand_tiles = random.sample(range(0, self.col * self.row), num_set)
        for value in rand_tiles:
            r, c = self.get_coordinates_from_num(value)
            self.tiles[c][r].set_fish(
                max(1, int(random.random() * Constants.MAX_FISH)))

    def get_coordinates_from_num(self, num):
        """
        Utility function to get the tile coordinates from a number.
        Used to randomly pick tiles from the board to set.
        A tile's number is it's column (zero-indexed) * rows in board + it's row

        :num: int           The tile's number
        :returns: tuple     The tile's row and col
        """
        col = math.floor(num / self.row)
        row = num % self.row
        return (row, col)

    def set_all(self, value):
        """
        Set all fish values for every tile in board equal to given value

        :value: int     The fish value to set
        """
        for col in range(0, self.col):
            for row in range(0, self.row):
                self.tiles[col][row].set_fish(value)

    def remove_tile(self, row, col):
        """
        Remove the tile at (row, col)

        :row: int      The row of the tile to remove
        :col: int      The column of the tile to remove
        """
        if self.tile_exists((row, col)):
            self.tiles[col][row].create_hole()

    def draw_board(self):
        """
        Draw the current game board using tkinter canvas.
        Pass functionality of drawing each tile to the Tile class.
        """
        w = (self.col * 4 + 1) * self.tiles[0][0].tile_size
        h = (self.row + 1) * self.tiles[0][0].tile_size
        canvas = Canvas(master, width=w, height=h)
        for c in range(0, self.col):
            for r in range(0, self.row):
                # need to draw at x and y
                self.tiles[c][r].draw_tile_fish(canvas)

        master.mainloop()
