from Fish.Admin.manager_interface import ManagerInterface
from Fish.Admin.referee import Referee
from Fish.Common.constants import MIN_PLAYERS, MAX_PLAYERS
from Fish.Remote.Adapters.extended_referee import ExtendedReferee
from Fish.Common.util import safe_call

"""
A Manager runs a Fish game tournament. A tournament are many games which are run
in succession for a collection of PlayerInterface (sorted by age), where each
subsequent round is run with the winners from the previous round.
Class fields of the Manager are:
    - queue: [List-of PlayerInterface], a list of players sorted by age (youngest to oldest)
        and represents the players who are currently still playing in the tournament
    - active_players: [Set PlayerInterface]
        represents the set of players who have not cheated or failed
    - previous_winners: [Set PlayerInterface]
        represents the winners from round N - 1, in the first round, this set is empty
    - games_in_previous_round: Natural
        represents the number of games that were run in the previous round, this is used for checking tournament completion
    - kicked_players: [Set PlayerInterface]
        represents players who have either cheated or failed (did not respond to messages)
    - referee_type: [Type Referee] or [Type Referee subclass]
        this is the type of the referee that will be used to run the games
    - timeout: Positive
        time in seconds to wait for each call to a player

A RoundResult is a Dictionary with keys: "winners", "losers", "kicked_players", where
    - "winners" is a [Set PlayerInterface]
    - "losers" is a [Set PlayerInterface]
    - "kicked_players" is a [Set PlayerInterface]
    - "games_played" is a Natural
and represents the winners, losers (non-winning players who followed the rules),
and kicked_players (those who broke the rules or timed out) for each round of the tournament,
and the number of games played in this round is represented by "games_played".
"""


class Manager(ManagerInterface):

    def __init__(self, referee_type=ExtendedReferee, timeout=1):
        """
        Constructor for a Referee who supervises one game.

        referee_type: Type  The type of Referee to use to run each game of Fish.
        timeout: Positive   Time in seconds to wait for each call to a player
        """
        self.__is_valid_referee_type(referee_type)

        self.__queue = []
        self.__active_players = set()
        self.__previous_winners = set()  # winners from round n - 1
        self.__games_in_previous_round = 0
        self.__kicked_players = set()
        self.__referee_type = referee_type
        self.__timeout = timeout

    def __is_valid_referee_type(self, referee_type):
        if not issubclass(referee_type, Referee):
            raise ValueError("referee_type must be Referee or a subclass of Referee")

    def run_tournament(self, players):
        self.__queue = players
        self.__active_players = set(players)
        self.__broadcast_tournament_start()

        while not self.__is_tournament_over():
            match_players = self.__make_rounds()
            round_result = self.__run_round(match_players)
            self.__update_bracket(round_result)

        self.__broadcast_tournament_end()

        return self.__get_tournament_result()

    def __update_bracket(self, round_result):
        """
        Add previous winners to a queue for the next round.
        Update the active players by removing kicked players.

        EFFECT: Updates active players and players playing in next round.

        RoundResult -> void
        """
        kicked_players = round_result["kicked_players"]
        self.__kick_players(kicked_players)
        self.__games_in_previous_round = round_result["games_played"]

        self.__previous_winners = set(self.__queue)
        self.__queue = list(filter(lambda p: p in round_result["winners"], self.__queue))

    def __kick_players(self, bad_players):
        """
        Removes the bad_players from the tournament.
        EFFECT: removes the bad_players from the active_players and the queue
                adds the bad_players to the set of kicked_players
        [Set PlayerInterface] -> void
        """
        self.__active_players = self.__active_players.difference(bad_players)
        self.__kicked_players.update(bad_players)
        self.__queue = list(filter(lambda p: p not in bad_players, self.__queue))

    def __run_round(self, match_players):
        """
        Runs one game match for each of the list of players in the given set.
        Returns the set of winners for this round.

        [List-of [List-of PlayerInterface]] -> RoundResult
        """
        round_result = {
            "winners": set(),
            "losers": set(),
            "kicked_players": set(),
            "games_played": len(match_players)
        }
        board_config = {"row": 5, "col": 3, "fish": 3}
        for players in match_players:
            ref = self.__referee_type(board_config)
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
        return set(self.__queue) == self.__previous_winners or \
            len(self.__queue) < MIN_PLAYERS or \
            self.__games_in_previous_round == 1

    def __broadcast_tournament_start(self):
        """
        Notifies all active players that the tournament is about to start. If the player fails to
        respond then they will be kicked.
        EFFECT: calls the tournament_start method on all active PlayerInterfaces in this tournament
                Players who fail to respond will be removed from the active_players and the queue
        void -> void
        """
        bad_players = set()
        for player in self.__active_players:
            response = safe_call(self.__timeout, player.tournament_start)
            if response is not True:
                bad_players.add(player)

        self.__kick_players(bad_players)

    def __broadcast_tournament_end(self):
        """
        Notifies all active players (those who have not failed or cheated) whether they
        have won or lost the game. Winners who fail to respond to the message become
        losers.

        EFFECT: calls the tournament_end method on all active PlayerInterfaces in this tournament
                Players who fail to respond will be removed from the active_players and the queue
        void -> void
        """
        bad_players = set()
        for player in self.__active_players:
            did_win = player in self.__queue
            response = safe_call(self.__timeout, player.tournament_end, [did_win])
            if response is False:
                bad_players.add(player)

        self.__kick_players(bad_players)

    def __get_tournament_result(self):
        """
        Return the list of players who won the tournament.

        void -> [List-of PlayerInterface]
        """
        return self.__queue
