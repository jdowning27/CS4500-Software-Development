from Tile import *
from Util import validate_non_neg_int, validate_pos_int
import math
import random
import sys

MAX = 5
SIZE = 20

class Board:

    def __init__(self, row, col):
        """
        Constructor that initializes the game board of size Row by Col
        """
        ## TODO: need to make these private
        self.tiles = [[None for r in range(0, row)] for c in range(0, col)]
        self.col = col
        self.row = row

    def init_board(self):
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
            print("usage: Invalid Input: holes + min > Total number of tiles")
            sys.exit(1)
        self.set_all(1)
        self.print_board()
        for h in holes:
            r, c = h
            self.remove_tile(r, c)
        self.print_board()
        self.set_random_tiles(self.col * self.row - (len(holes) + min))
        self.print_board()


    def create_board_without_holes(self, fish):
        self.init_board()
        validate_pos_int(fish)
        self.set_all(fish)

    def get_all_reachable_posn(self, row, col):
        # get all tiles surrounding given tile
        # TODO: note that these row and col are for index, 0-indexed
        result = []
        result.extend(self.get_reachable_posn_dir(row, col, Tile.get_north_coord))
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

        :returns: array of reachable tiles to the give direction
        """
        next_tile = get_dir_coord(self.tiles[col][row])
        if self.tile_exists(next_tile):
            result = [next_tile]
            result.extend(self.get_reachable_posn_dir(next_tile[0], next_tile[1], get_dir_coord))
            return result
        else:
            return []
    
    def tile_exists(self, tile_coords):
        """
        Is the tile in bounds and active?

        :returns: bool      True if the tile exists, and is active
        """
        row, col = tile_coords
        return row >= 0 and row < self.row and col >= 0 and col < self.col and self.tiles[col][row].is_active


    def set_random_tiles(self, num_set):
        rand_tiles = random.sample(range(0, self.col * self.row), num_set)
        for value in rand_tiles:
            r, c = self.get_coordinates_from_num(value)
            self.tiles[c][r].set_fish(max(1, int(random.random() * MAX)))

    def get_coordinates_from_num(self, num):
        col = math.floor(num / self.row)
        row = num % self.row
        return (row, col)

    def set_all(self, value):
        for col in range(0, self.col):
            for row in range(0, self.row):
                self.tiles[col][row].set_fish(value)

    def remove_tile(self, row, col):
        self.tiles[col][row].create_hole()

    
    def print_board(self):
        for c in range(0, self.col):
            arr = [None] * self.row
            for r in range(0, self.row):
                arr[r] = self.tiles[c][r].fish
    
    def draw_board(self):
        w = (self.col * 4 + 1) * SIZE
        h = (self.row * 3 + 1) * SIZE
        canvas = Canvas(master, width=w, height=h)
        for c in range(0, self.col):
            for r in range(0, self.row):
                # need to draw at x and y
                self.tiles[c][r].draw_tile_fish(SIZE, canvas)

        master.mainloop()