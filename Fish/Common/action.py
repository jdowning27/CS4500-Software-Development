class Action:
    """
    Represents an action in the game tree that leads to the next
    game state.
    """

    def __eq__(self, other):
        pass

    def apply_move(self, tree):
        """
        Applies itself to the given state and returns the resulting state
        Move is expected to be valid in game

        :tree: GameTree	    Origin GameTree
        :returns: State	    State with this action applied
        """
        pass

    def break_tie(self, other):
        """
        Breaks the tie between actions by returning the action with the lowest
        row index. If row is the same, take the action with lowest column index.
        If actions are equal, return this action

        :returns: Move        The action with the lowest row/col number
        """
        pass

    def print_json(self):
        """
        Return a JSON value representation of this move.

        "return" JSON value
        """
        pass
