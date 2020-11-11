"""
The interface for Game. A Game is one of GameSetup, GameTree, GameEnded.
"""
class Game:

    def has_game_ended(self):
        """
        The game has ended when the type is of GameEnded or there are no possible moves left in GameTree.

        :returns: Boolean	True if game over otherwise false
        """
        pass

    def get_winners(self):
        """
        Returns the list of winners of the game if they exist. If the game is not over returns false.

        :returns: Maybe List of Players		Players who have won
        """
        pass

    def copy(self):
        """
        Returns a copy of the Game.

        :returns: Game
        """
        pass
