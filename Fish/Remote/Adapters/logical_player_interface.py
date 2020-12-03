
class LogicalPlayerInterface:
    """
    This interface represents the protocol defined by the course website
    It will be used by our proxy components to run Fish.com tournaments
    """

    def start(starting):
        """
        Notifies the player that the tournament is about to start

        Boolean -> Void
        """
        pass

    def end(did_win):
        """
        Notifies the player that the tourmanet is over.
        if did_win is True the player won, otherwise the player lost

        Boolean -> Void
        """
        pass

    def play_as(color):
        """
        Tells the player what color they will be playing as this game

        Color -> Void
        """
        pass
    
    def play_with(colors):
        """
        Tells the player the colors that their opponents will be playing as

        [List-of Color] -> Void
        """
        pass

    def setup(state):
        """
        Gives the player a state and asks them to make a placement. 
        The placement is given as a (row, col) tuple.

        State -> Posn
        """
        pass

    def tt(state, actions):
        """
        The player is given the current state and the list of actions since 
        they were last called and asked to make a move. The player must return
        an action that represents their move. If no move is available a skip is returned

        State, Actions[] -> Move | Skip
        """
        pass