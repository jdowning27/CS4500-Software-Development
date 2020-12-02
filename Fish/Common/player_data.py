from Fish.Common.util import validate_non_neg_int, print_error
from Fish.Common.color import Color

"""
The internal representation of a player which keeps track of its
penguin color, age, and an array of penguins.
"""
class PlayerData:
    def __init__(self, color, age=0, score=0):
        if type(color) is not Color:
            raise ValueError("Invalid color")
        self.__color = color
        self.__age = age
        self.__penguins = []
        self.__score = score

    def __eq__(self, other):
        return type(other) is PlayerData and self.__color == other.get_color() and \
            self.__age == other.get_age() and self.__penguins.sort() == other.get_penguins().sort()
        
    def get_penguins(self):
        """
        Getter for list of penguins for this player
        """
        return self.__penguins
        
    def copy(self):
        """
        Makes a deep copy of this player

        :returns: PlayerData	Copy of this PlayerData
        """
        new_player = PlayerData(self.__color, self.__age, self.__score)
        for penguin in self.__penguins:
            new_player.add_penguin(penguin)
        return new_player

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

    def get_age(self):
        """
        Getter for this Player's age

        :returns: int       Positive integer representing the Player's age
        """
        return self.__age

    def move_penguin(self, from_posn, to_posn):
        """
        Move the penguin at from_posn to to_posn if the from_posn
        exists in this penguin.
        """
        if from_posn in self.__penguins:
            self.__penguins = [to_posn if p == from_posn else p for p in self.__penguins]

    def get_score(self):
        return self.__score

    def add_to_score(self, fish):
        self.__score += fish

    def print_json(self):
        """
        Returns json representation of the player

        :returns: dictionary	json representation of player
        """
        player = {}
        player['color'] = self.__color.value
        player['score'] = self.__score
        places = []
        for penguin in self.__penguins:
            places.append([penguin[0], penguin[1]])
        player['places'] = places
        return player
