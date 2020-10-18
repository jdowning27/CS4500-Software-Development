import math
import random
import sys

from Tile import *
from Util import validate_non_neg_int, validate_pos_int, print_error
from Constants import MAX_FISH, GUI_UNIT



"""
Represents the Fish Game board that is made up of hexagonal tiles.
"""
class Board:

    def __init__(self, row, col):
        """
        Constructor that initializes the game board of size Row by Col

        :row: int       The number of rows
        :col: int       The number of columns
        """
        
        validate_pos_int(row, col)
        self.tiles = [[None for r in range(0, row)] for c in range(0, col)]
        self.col = col
        self.row = row

    def __eq__(self, other):
        return type(other) is Board and self.row == other.row and self.col == other.col and self.tiles == other.tiles

    def init_board(self):
        """
        Intializes the game board with Tile objects in each place
        """
        for c in range(0, self.col):
            for r in range(0, self.row):
                self.tiles[c][r] = Tile(r, c)

    def copy(self):
        """
        Creates a deep copy of the board.

        :returns:Board		Copy of this board
        """
        new_tiles = [[self.tiles[c][r].copy() for r in range(0, self.row)] for c in range(0, self.col)]
        new_board = Board(self.row, self.col)
        new_board.tiles = new_tiles
        return new_board

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
        for h in holes:
            r, c = h
            self.remove_tile(r, c)
        self.set_random_tiles(self.col * self.row - (len(holes) + min))

    def create_board_without_holes(self, fish):
        """
        Create board with no holes, and set all tiles to have a specific
        number of fish.

        :fish: int          The number of fish per tile
        """
        self.init_board()
        validate_pos_int(fish)
        self.set_all(fish)

    def create_board_from_json(self, board_array):
        """
        Create a board with fish and holes when the number of fish is 0.
        If the nested list of fish values is shorter than the row length,
        the remaining tiles are holes. 
        The given 2d-array is structed as follows, where each int represents
        the number of fish:
        [
            [   1,     2,      3       ],
            [       4,     0,      5   ]
        ]
        """
        for r in range(0, self.row):
            for c in range(0, self.col):
                # get the fish count for this tile
                fish = self.__get_fish(board_array, r, c)
                self.tiles[c][r] = Tile(r, c)
                if fish == 0:
                    self.remove_tile(r, c)
                else:
                    self.tiles[c][r].set_fish(fish)


    def __get_fish(self, board_array, r, c):
        """
        Helper function for translating 2D array to board tiles.
        :board_array: array     2D array of fish values
        :r: int                 the row of the tile
        :c: int                 the column of the tile
        """
        if c >= len(board_array[r]):
            return 0
        else:
            return board_array[r][c]


    def get_all_reachable_posn(self, row, col):
        """
        Get all reachable board positions from (row, col)

        :returns: array     List of (row, col) representing all possible reachable positions
        """
        result = []
        result.extend(self.get_reachable_posn_dir(
            row, col, Tile.get_north_coord))
        result.extend(self.get_reachable_posn_dir(row, col, Tile.get_south_coord))
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
            result.extend(self.get_reachable_posn_dir(*next_tile, get_dir_coord))
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
                max(1, int(random.random() * MAX_FISH)))

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

    def get_offset(self, row, col):
        """
        Get the (x, y) offset to draw an image on tkinter.Canvas. Image could be
        Tile, a penguin, or fish.

        :row: int           The row of the image
        :col: int           The column of the image

        :returns: tuple     The (x, y) pixel offset to draw at
        """
        size = GUI_UNIT * MAX_FISH
        x_off = 4 * size * col
        if not is_even(row):
            x_off += 2 * size
        y_off = size * row
        return (x_off, y_off)

    def get_dimensions(self):
        """
        Get dimensions for this board to be able to create tkinter.Canvas

        :returns: tuple     Representing the (width, height) of the canvas
        """
        size = GUI_UNIT * MAX_FISH
        w = (self.col * 4 + 1) * size
        h = (self.row + 1) * size
        return (w, h)

    def draw_board(self, canvas):
        """
        Draw the current game board using tkinter canvas.
        Pass functionality of drawing each tile to the Tile class.

        :canvas: tkinter.Canvas     The canvas to draw on
        :returns: tkinter.Canvas    The canvas with tiles, fish, holes
        """
        for c in range(0, self.col):
            for r in range(0, self.row):
                # need to draw at x and y
                offset = self.get_offset(r, c)
                self.tiles[c][r].draw_tile_fish(canvas, offset)
        return canvas


    def draw_penguin(self, canvas, color, posn):
        """
        Draw the penguin at on the canvas at given positions with given color.

        :canvas: tkinter.Canvas     The canvas to draw on
        :returns: tkinter.Canvas    The canvas with penguins
        """
        size = GUI_UNIT * MAX_FISH
        offset_x, offset_y = self.get_offset(*posn)
        # Penguins are rectangles, center them on the tiles
        x0 = offset_x + 1.5 * size - GUI_UNIT
        x1 = offset_x + 1.5 * size + GUI_UNIT
        y0 = offset_y + size - GUI_UNIT
        y1 = offset_y + size + GUI_UNIT
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        return canvas

    def print_json(self):
        """
        Returns json representation of the board

        :returns: [][]int	2d array of board with fish values
        """
        board = []
        for r in range(0, self.row):
            row = []
            for c in range(0, self.col):
                row.append(self.tiles[c][r].get_fish())
            board.append(row)
        return board
