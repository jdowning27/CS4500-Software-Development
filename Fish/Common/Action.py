
"""
Represents a game action.
- Holds the starting coordinate of penguin being moved
- Holds where it is moved to
"""

class Action:

    def __init__(self, from_posn, to_posn):
        self.__from_posn = from_posn
        self.__to_posn = to_posn

    def __eq__(self, other):
        return type(other) is type(self) and self.__from_posn == other.get_from_posn() and \
            self.__to_posn == other.get_to_posn()

    def __hash__(self):
        return (self.__from_posn, self.__to_posn).__hash__()

    def get_from_posn(self):
        return self.__from_posn

    def get_to_posn(self):
        return self.__to_posn

    def apply_move(self, state):
        """
        Applies itself to the given state and returns the resulting state
        Action is expected to be valid in game

        :state: State	Origin State
        :returns: State	Moved State
        """
        return state.move_penguin(self.__from_posn, self.__to_posn)
