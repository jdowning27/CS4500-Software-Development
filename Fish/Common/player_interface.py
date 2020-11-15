
"""
Represents a player interface. Different kinds of players
may implement this interface, such as AI or Remote players.
Classes that implement this interface must override these methods.
"""
class PlayerInterface:

    def set_state(self, state):
        """
        Sets the player's Game representation using the given State.

        State -> void
        """
        pass

    def choose_next_move(self):
        """
        Choose next move in the Game. The player is responsible for keeping
        track of their own instance of Game.
        A player may choose to optimize for specific moves.

        void -> Action
        """
        pass
    
    def choose_placement(self, state):
        """
        Return the position (row, col) of where to place a penguin for this player.

        :state: State           The state to place penguins on
        :returns: (int, int)
        """
        pass

    def assign_color(self, player_color):
        """
        Assign a Color to the player. Set player.__color to player_color

        :player_color: Color        The color of this player
        """
        pass

    def game_over(self, game_result):
        """
        Let the Player know that the game has ended.

        GameResult -> void
        """
        pass

    def update_with_action(self, action):
        """
        Update the Player's local Game with the given action

        Action -> void
        """
        pass

    def get_color(self):
        """
        Returns this Player's color

        void -> Color
        """
        pass

    def tournament_start(self):
        """
        Used by the tournament manager to notify this player that the tournament is starting
        Players must return True to indicate they are ready to start the tournament
        void -> Boolean
        """
        pass

    def tournament_end(self, result):
        """
        Used by the tournament manager to notify the players that the tournament is over and if they
        have won or lost.
        Players must return True to indicate they they have received the message.
        String -> Boolean
        """
        pass
