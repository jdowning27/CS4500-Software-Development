"""
keep winners for each round
a list of active players (non failing cheating players)
    - need to make sure to remove kicked players after each game
after winners are reported, they need to respond/accept the message
"""
from manager_interface import ManagerInterface
"""
#TODO manager interpretation

A RoundResult is a Dictionary with keys: "winners", "losers", "kicked_players", where
    - "winners" is a [Set PlayerInterface]
    - "losers" is a [Set PlayerInterface]
    - "kicked_players" is a [Set PlayerInterface]
and represents the winners, losers (non-winning players who followed the rules), 
and kicked_players (those who broke the rules or timed out) for each round of the tournament.
"""
class Manager(ManagerInterface):

    def __init__(self):
        self.__queue = []
        self.__active_players = set()
        self.__previous_winners = set() # winners from round n - 1
        self.__kicked_players = set()


    def run_tournament(self, players):
        while not self.__is_tournament_over():
            match_players = self.__make_rounds()
            round_result = self.__run_round(match_players)
            self.__update_bracket(round_result)

    def __update_bracket(self, round_result):
        """
        Add previous winners to a queue for the next round.
        Update the active players by removing kicked players.

        EFFECT: Updates active players and players playing in next round.

        RoundResult -> void
        """
        self.__previous_winners = self.__queue
        self.__queue = round_result["winners"]

        kicked_players = round_result["kicked_players"]
        self.__active_players = self.__active_players.difference(kicked_players)
        self.__kicked_players.update(kicked_players)

    def __run_round(self, match_players):
        """
        Runs one game match for each of the list of players in the given set.
        Returns the set of winners for this round.

        [List-of [List-of PlayerInterface]] -> RoundResult
        """
        round_result = {
            "winners": set(),
            "losers": set(),
            "kicked_players": set()
        }
        for players in match_players:
            ref = Referee()
            game_result = ref.play_game(players)
            round_result["winners"].update(game_result["winners"])
            round_result["losers"].update(game_result["losers"])
            round_result["kicked_players"].update(game_result["kicked_players"])
        return round_result

    def __make_rounds(self):
        """
        Split the current queue into matches of MIN_PLAYERS to MAX_PLAYERS.

        Starts by assigning players to games with the MAX_PLAYERS number of players.
        When the number of remaining players is less than MIN_PLAYERS, backtrack
        by one game and try to form games with MAX_PLAYERS - 1 until all players
        are assigned.

        Assume that there are at least MIN_PLAYERS in the queue.

        void -> [List-of [List-of PlayerInterface]]
        """
        num_players = len(self.__queue)
        if num_players < MIN_PLAYERS:
            raise ValueError("Not enough players to run another round.")

        match_players = []
        current_match = []
        for index in range(0, num_players, MAX_PLAYERS):
            current_match = self.__queue[index:index + MAX_PLAYERS]
            match_players.append(current_match)

        match_players = self.__balance_games(match_players)
        return match_players

    def __balance_games(self, match_players):
        """
        Balance the number of players in each game so that each game has between
        MIN_PLAYERS and MAX_PLAYERS.

        [List-of [List-of PlayerInterface]] -> [List-of [List-of PlayerInterface]]
        """
        last_game = match_players[-1]
        if len(match_players) <= 1 or len(last_game) >= MIN_PLAYERS:
            return match_players

        else:
            second_last = match_players[-2]
            last_two = second_last + last_game
            len_last_two = len(last_two)
            match_players[-2] = last_two[:len_last_two - MIN_PLAYERS]
            match_players[-1] = last_two[-MIN_PLAYERS:]
            return match_players
        
            


    def __is_tournament_over(self):
        """
        Determines if the tournament is over.
        The tournament has ended when:
            - Two sequential rounds produce the same winners
            - There are too few (< MIN_PLAYERS) players for a single game
            - When there are few enough participants to run a single game. 
                This game is run, and the winners of this game are the winners of the tournament.

        void -> Boolean
        """
        pass

    def __message_players(self):
        """
        Notifies all active players (those who have not failed or cheated) whether they
        have won or lost the game. Winners who fail to respond to the message become
        losers.

        void -> void
        """
        pass