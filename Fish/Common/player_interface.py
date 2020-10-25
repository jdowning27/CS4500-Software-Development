
class PlayerInterface:

    def remove_penguins(self):
        """
        Removes all of this players penguins. Called when player has violated rules.

        :returns: void
        """
        pass

    def get_age(self):
        """
        Returns the player's age.

        :returns: Natural Number	Player's age
        """
        pass

    def get_color(self):
        """
        Returns player's assigned color.

        :returns: Color		Player's assigned color
        """
        pass

    def get_penguins(self):
        """
        Gets a set of the position of all of the player's penguins.

        :returns: Set of (row, col)		Set of penguin positions
        """
        pass

    def get_score(self):
        """
        Returns player's score.

        :returns: Natural Number	Player's score
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

    def choose_next_move(self, moves):
        """
        Choose next move from a dictionary of potential actions and resulting GameTrees.
        A player may choose to optimize for specific moves.

        :moves: {Move: GameTree}		Dictionary of available moves and their resulting GameTrees.
        :returns: Move			Player's chosen action
        """
        pass
