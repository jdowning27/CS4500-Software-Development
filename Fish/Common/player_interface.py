
"""
Represents a player interface. Different kinds of players
may implement this interface, such as AI or Remote players.
Classes that implement this interface must override these methods.
"""
class PlayerInterface:

    def choose_next_move(self, tree):
        """
        Choose next move in this GameTree.
        A player may choose to optimize for specific moves.

        :tree: GameTree		        Current GameTree
        :returns: Move			Player's chosen action
        """
        pass
    
    def place_penguin(self, state):
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

    def move_penguin(self, from_posn, to_posn, fish):
        """
        Moves the player's penguin located at from_posn to to_posn. Add fish to the player's score.
        The referee only calls this function if it is a legal move.

        :from_posn: (Nat, Nat)		(row,col)Location of penguin to be moved
        :to_posn: (Nat, Nat)		(row, col)Location where the penguin will be moved to
        :fish: Positive Int		Fish to add to player's score
        :returns: void
        """
        pass

    def remove_penguins(self):
        """
        Removes all of this players penguins. Called when player has violated rules.

        :returns: void
        """
        pass

    def game_over(self, state):
        """
        Let the Player know that the game has ended.

        :state: State       The last state of the game
        :returns: void
        """
        pass

    def get_age(self):
        """
        Returns the player's age.

        :returns: Natural Number	Player's age
        """
        pass
