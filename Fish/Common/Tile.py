from Util import is_even
from tkinter import *
from Constants import GUI_UNIT, MAX_FISH

master = Tk()

class Tile:

    def __init__(self, row, col):
        ## TODO: revisit public/private of class variables
        self.fish = None
        self.is_active = True
        self.row = row
        self.col = col
        self.tile_size = GUI_UNIT * MAX_FISH

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
            
    def get_points(self, offset):
        """
        Gets the coordinates for each point on a hexagon of a certain size

        :size: int    Size of Hexagon
        :return: array    List of points on hexagon
        """
        x_off, y_off = offset
        points = [self.tile_size, 0,
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
        canvas.create_polygon(self.get_points(offset), outline='white', fill=color, tags="hex")
        canvas.pack()

    def draw_tile_fish(self, canvas):
        offset = self.get_offset()
        self.draw_tile(canvas, offset)
        self.draw_fish(canvas, offset)

    def draw_fish(self, canvas, offset):
        x_off, y_off = offset

        for i in range(0, self.fish):
            self.draw_single_fish(canvas, offset, i)

    def draw_single_fish(self, canvas, offset, i):
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


    def get_offset(self):
        x_off = 4 * self.tile_size * self.col
        if not is_even(self.row):
            x_off += 2 * self.tile_size

        y_off = (self.tile_size * self.row)

        return (x_off, y_off)
