from Util import is_even
from tkinter import *

master = Tk()

class Tile:

    def __init__(self, row, col):
        ## TODO: revisit public/private of class variables
        self.fish = None
        self.is_active = True
        self.row = row
        self.col = col

    def create_hole(self):
        self.is_active = False
        self.fish = 0

    def set_fish(self, fish):
        if self.is_active:
            self.fish = fish      

    def get_north_coord(self):
        return (self.row - 2, self.col)
    
    def get_south_coord(self):
        return (self.row + 2, self.col)

    def get_nw_coord(self):
        if is_even(self.row):
            return (self.row - 1, self.col - 1)
        else:
            return (self.row - 1, self.col)
    
    def get_ne_coord(self):
        if is_even(self.row):
            return (self.row - 1, self.col)
        else:
            return (self.row - 1, self.col + 1)
    
    def get_sw_coord(self):
        if is_even(self.row):
            return (self.row + 1, self.col - 1)
        else:
            return (self.row + 1, self.col)

    def get_se_coord(self):
        if is_even(self.row):
            return (self.row + 1, self.col)
        else:
            return (self.row + 1, self.col + 1)
            
    def get_points(self, size):
        """
        Gets the coordinates for each point on a hexagon of a certain size

        :size: int    Size of Hexagon
        :return: array    List of points on hexagon
        """
        return [size, 0, size * 2, 0, 3 * size, size, 2 * size, 2 * size, size, 2 * size, 0, size]
        
    def draw_tile(self, points, canvas):
        """
        Draw the hexagon on the given canvas using the points

        :points: array              X, Y coordinates of the hexagon's points
        :canvas: tkinter.Canvas     Canvas to draw on
        """
        canvas.create_polygon(points, fill='red', tags="hex")
        canvas.pack()

    def draw_tile_fish(self, size, canvas):
        points = self.get_points(size)
        self.draw_tile(points, canvas)



