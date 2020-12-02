from Fish.Common.action import Action
from Fish.Common.skip import Skip
"""
Represents a game action when the penguin is moved.
- Holds the starting coordinate of penguin being moved
- Holds where it is moved to
"""
class Move(Action):

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

    def apply_move(self, tree):
        """
        Applies itself to the given state and returns the resulting state
        Move is expected to be valid in game

        :tree: GameTree	    Origin GameTree
        :returns: State	    GameTree with this action applied
        """
        return tree.state.move_penguin(self.__from_posn, self.__to_posn)

    def break_tie(self, other):
        """
        Breaks the tie between actions by returning the action with the lowest
        row index. If row is the same, take the action with lowest column index.
        If actions are equal, return this action

        :returns: Move        The action with the lowest row/col number
        """
        if type(other) is Skip:
            return self
        from_row, from_col = self.__from_posn
        other_from_row, other_from_col = other.get_from_posn()
        to_row, to_col = self.__to_posn
        other_to_row, other_to_col = other.get_to_posn()
        if from_row < other_from_row:
            return self
        elif from_row > other_from_row:
            return other
        elif from_col < other_from_col:
            return self
        elif from_col > other_from_col:
            return other
        elif to_row < other_to_row:
            return self
        elif to_row > other_to_row:
            return other
        elif to_col < other_to_col:
            return self
        elif to_col > other_to_col:
            return other
        else:
            return self

    def print_json(self):
        return [self.__from_posn, self.__to_posn]
        
