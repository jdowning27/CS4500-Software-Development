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

        :returns: [Maybe [List-of Player]]		Players who have won
        """
        pass

    def copy(self):
        """
        Returns a copy of the Game.

        :returns: Game
        """
        pass

    def get_players_score(self, player_color):
        """
        returns the score of the player given by color
        Color -> Integer
        """
        pass

    def get_possible_actions(self):
        """
        Get the possible actions from the Game.
        Only GameTree will result in a non-empty list. 

        void -> [List-of Action]
        """
        pass

    def get_current_player_color(self):
        """
        Get the color of the current player.

        void -> [Maybe Color]
        """
        pass