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

    def run_tournament(self, players):
        """
        Run the Fish game tournament to completion. Returns a list of tournament winners.

        The tournament ends when one of the following conditions is met:
            - Two sequential rounds produce the same winners
            - There are too few (< MIN_PLAYERS) players for a single game
            - When there are few enough participants to run a single game. 
                This game is run, and the winners of this game are the winners of the tournament.

        This tournament manager notifies players whether they won or lost the tournament.
        Winners who fail to accept this message become losers.

        [List-of PlayerInterface] -> [List-of PlayerInterface]
        """
        pass

    def observer_signup(self, tcp_address):
        """
        Allows observers to signup to be alerted to ongoing tournament statistics.

        :tcp_address: int
        :returns: void
        """
        pass
