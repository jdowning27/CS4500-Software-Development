"""
The data representation for a tournament manager.
The tournament manager communicates with thousands of players and spectators to run one tournament
of the fish game where a tournament is several rounds of the game until there is one winner.
It accepts a list of players who will play in the tournament
The tournament manager creates many Referees who each manage a game with the
players the tournament manager assigns to it.
It collects tournament statistics at the end of each game and informs observers of game outcomes.

"""
class ManagerInterface:

    def observer_signup(self, tcp_address):
        """
        Allows observers to signup to be alerted to ongoing tournament statistics.

        :tcp_address: int
        :returns: void
        """
        pass

    def leave_tournament(self, player):
        """
        Allows player to leave the tournament.

        :player:	Player who wants to leave tournament
        :returns: void
        """
        pass


