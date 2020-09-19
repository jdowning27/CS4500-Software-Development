#!/usr/bin/env python

import sys
from tkinter import *

master = Tk()


def verify_input(args):
    """
    Checks that the given list of arguments is valid

    :args: array     List of command line arguments  
    :returns:      Returns argument if input is valid and false if not
    """
    if len(args) != 1:
        raise Exception("Invalid number of arguments")
    try:
        i = int(args[0])
        if i > 0:
            return i
        else:
            raise Exception("Input needs to be > 0")
    except ValueError:
        raise ValueError("Invalid input type")


def get_points(size):
    """
    Gets the coordinates for each point on a hexagon of a certain size

    :size: int    Size of Hexagon
    :return: array    List of points on hexagon
    """
    return [size, 0, size * 2, 0, 3 * size, size, 2 * size, 2 * size, size, 2 * size, 0, size]

def quit(event):
    master.destroy()    

def main():
    size = verify_input(sys.argv[1:])
    if size:
        # Draw Hexagon
        
        #master = Tk()
        canvas = Canvas(master, width=3*size, height=2*size)
        canvas.pack()
        points = get_points(size)
        hex = canvas.create_polygon(points, fill='red', tags="hex")
        canvas.tag_bind("hex", "<Button-1>", quit)
        canvas.pack()
        master.mainloop()
    else:
        # Print error
        print("error")
        return 1
