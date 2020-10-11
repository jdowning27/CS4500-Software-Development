"""
The internal representation of a player which keeps track of its
penguin color, age, and an array of penguins.
"""
class Player:
    def __init__(self, color, age):
        # TODO check age is positive int and check color is instance of Color
        self.__color = color
        self.__age = age
        self.__penguins = []
        
    def get_penguins(self):
        """
        Getter for list of penguins for this player
        """
        return self.__penguins
        
    def add_penguin(self, posn):
        """
        Add penguin to this Player's list of penguins with
        posn (row, col)

        :posn: tuple        The (row, col) position for the penguin
        """
        self.__penguins.append(posn)

    def get_color(self):
        """
        Getter for this Player's assigned color

        :returns: enum Color    
        """
        return self.__color

    def move_penguin(self, from_posn, to_posn):
        """
        Move the penguin at from_posn to to_posn if the from_posn
        exists in this penguin.
        """
        if from_posn in self.__penguins:
            self.__penguins.remove(from_posn)
            self.add_penguin(to_posn)
