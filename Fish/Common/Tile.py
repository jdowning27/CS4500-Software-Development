

class Tile:

    def __init__(self):
        self.fish = None
        self.is_active = True

    def create_hole(self):
        self.is_active = False

    def set_fish(self, fish):
        self.fish = fish
