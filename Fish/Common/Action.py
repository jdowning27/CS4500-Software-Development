"""
Represents an action in the game tree that leads to the next
game state.
"""
class Action:

    def __eq__(self, other):
        pass

    def apply_move(self, tree):
        pass

    def break_tie(self, other):
        pass