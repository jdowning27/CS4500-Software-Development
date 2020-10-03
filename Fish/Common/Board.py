import Tile
import math
import random
import sys

MAX = 5

class Board:

    def __init__(self, row, col):
        self.tiles = [Tile() * row] * col
        self.col = col
        self.row = row

    def create_board_with_holes(self, holes, min):
        validate_non_neg_int(len(holes), min)
        if len(holes) + min > (self.row * self.col):
            print("usage: Invalid Input: holes + min > Total number of tiles")
            sys.exit(1)
        for h in holes:
            r, c = h
            remove_tile(r, c)
        set_all(1)
        set_random_tiles(self.col * self.row - (len(holes) + min))

    def create_board_without_holes(self, fish):
        validate_pos_int(fish)
        set_all(fish)

    def set_random_tiles(self, num_set):
        rand_tiles = random.sample(range(0, self.col * self.row), num_set)
        for value in rand_tiles:
            r, c = get_coordinates_from_num(value)
            self.tiles[c][r].set_fish(random(range(1, MAX)))

    def get_coordinates_from_num(self, num):
        col = math.floor(num / self.col)
        row = num % self.col
        return (row, col)

    def set_all(self, value):
        for col in self.tiles:
            for tile in col:
                tile.set_fish(value)

    def remove_tile(self, row, col):
        self.tiles[col][row].create_hole()

    def validate_non_neg_int(*args):
        for arg in args:
            validate_int(arg)
            if arg < 0:
                print("usage: must be non negative int")
                sys.exit(1)

    def validate_pos_int(*args):
        for arg in args:
            validate_int(arg)
            if arg <= 0:
                print("usage: must be positive int")
                sys.exit(1)

    def vaidate_int(arg):
        try:
            int(arg)
        except ValueError:
            print("usage: must be integer")
            sys.exit(1)
