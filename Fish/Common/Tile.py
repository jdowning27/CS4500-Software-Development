from Util import is_even
from Constants import GUI_UNIT, MAX_FISH

class Tile:

    def __init__(self, row, col):
        """
        Constructor for Tile class.

        :row: int           The tile's row
        :col: int           The tile's column

        :fish: int          The number of fish this tile has, initially none
        :is_active: bool    Is the tile active? (has not been removed from board)
        :tile_size: int     Pixel size to use in drawing
        """
        self.fish = None
        self.is_active = True
        self.row = row
        self.col = col
        self.tile_size = GUI_UNIT * MAX_FISH

    def create_hole(self):
        """
        Creates a whole at this Tile. 
        Set is_active to False, and get rid of fish.
        """
        self.is_active = False
        self.fish = 0

    def copy(self):
        """
        Create a deep copy of this tile

        :returns: Tile		Copy of this tile
        """
        new_tile = Tile(self.row, self.col)
        new_tile.fish = self.fish
        new_tile.is_active = self.is_active
        return new_tile

    def set_fish(self, fish):
        """
        Set the number of fish equal to given number.
        Only set the fish count if the Tile is active

        :fish: int      The number of fish to set to
        """
        if self.is_active:
            self.fish = fish

    def get_north_coord(self):
        """
        Get the coordinate (row, col) of the Tile north of this Tile
        """
        return (self.row - 2, self.col)

    def get_south_coord(self):
        """
        Get the coordinate (row, col) of the Tile south of this Tile
        """
        return (self.row + 2, self.col)

    def get_nw_coord(self):
        """
        Get the coordinate (row, col) of the Tile northwest of this Tile
        """
        if is_even(self.row):
            return (self.row - 1, self.col - 1)
        else:
            return (self.row - 1, self.col)

    def get_ne_coord(self):
        """
        Get the coordinate (row, col) of the Tile northeast of this Tile
        """
        if is_even(self.row):
            return (self.row - 1, self.col)
        else:
            return (self.row - 1, self.col + 1)

    def get_sw_coord(self):
        """
        Get the coordinate (row, col) of the Tile southwest of this Tile
        """
        if is_even(self.row):
            return (self.row + 1, self.col - 1)
        else:
            return (self.row + 1, self.col)

    def get_se_coord(self):
        """
        Get the coordinate (row, col) of the Tile southeast of this Tile
        """
        if is_even(self.row):
            return (self.row + 1, self.col)
        else:
            return (self.row + 1, self.col + 1)

    def get_hex_points(self, offset):
        """
        Gets the coordinates for each point on a hexagon of a certain size

        :size: int    Size of Hexagon
        :return: array    List of points on hexagon
        """
        x_off, y_off = offset
        points = [
            self.tile_size, 0,
            self.tile_size * 2, 0,
            3 * self.tile_size, self.tile_size,
            2 * self.tile_size, 2 * self.tile_size,
            self.tile_size, 2 * self.tile_size,
            0, self.tile_size]

        for p in range(0, len(points)):
            if is_even(p):
                points[p] += x_off
            else:
                points[p] += y_off

        return points

    def draw_tile(self, canvas, offset):
        """
        Draw the hexagon on the given canvas using the points

        :points: array              X, Y coordinates of the hexagon's points
        :canvas: tkinter.Canvas     Canvas to draw on
        """
        color = 'orange' if self.is_active else 'gray'
        canvas.create_polygon(self.get_hex_points(offset), outline='white', fill=color)
        canvas.pack()

    def draw_tile_fish(self, canvas, offset):
        """
        Draw the tile on given canvas at offset with all the fish.

        :canvas: tkinter.Canvas         The canvas to draw on
        :offset: tuple                  The (x, y) pixel offset to draw this tile
        """
        self.draw_tile(canvas, offset)
        self.draw_fish(canvas, offset)

    def draw_fish(self, canvas, offset):
        """
        Draw all the fish on the canvas
        """
        for i in range(0, self.fish):
            self.draw_single_fish(canvas, offset, i)

    def draw_single_fish(self, canvas, offset, i):
        """
        Draw single fish on the canvas. 
        A fish image is an Oval with a Triangle tail.

        :canvas: tkinter.Canvas     The canvas to draw on
        :offset: tuple              The (x, y) offset to draw this Tile
        :i:      int                The index to draw fish vertically aligned
        """
        x_off, y_off = offset

        x0 = self.tile_size + x_off
        y0 = i * (1.5 * GUI_UNIT) + y_off + (GUI_UNIT)
        x1 = 2 * self.tile_size + x_off
        y1 = y0 + (GUI_UNIT)
        canvas.create_oval(x0, y0, x1, y1, fill='blue')

        points = [x1, y0 + (.5 * GUI_UNIT),
                  x1 + (.25 * GUI_UNIT), y0,
                  x1 + (.25 * GUI_UNIT), y1]
        canvas.create_polygon(points, fill='blue')
