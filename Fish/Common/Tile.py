from Util import is_even

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


