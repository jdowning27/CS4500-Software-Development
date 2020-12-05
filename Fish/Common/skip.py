from Fish.Common.action import Action
"""
Represents an action by a Player where no move is possible.
Skip this player's turn, and the game state remains the same.
"""
class Skip(Action):

    def __eq__(self, other):
        return type(other) is Skip  

    def __ne__(self, other):
        return type(other) is not Skip

    def __hash__(self):
        return "skip".__hash__()

    def apply_move(self, tree):
        """
        Return a copy of the same state with next player's turn
        """
        new_state = tree.state.copy()
        new_state.set_next_players_turn()
        return new_state

    def break_tie(self, other):
        """
        Usage: this function should not be called on this object.
        This object should only be used when there are no other
        moves for this player on the board
        """
        return other
    
    def print_json(self):
        return False
