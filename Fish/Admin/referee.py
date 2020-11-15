from player_data import PlayerData
from color import Color
from board import Board
from state import State
from skip import Skip
from game_tree import GameTree
from game_setup import GameSetup
from game_ended import GameEnded
from util import get_max_penguin_count
"""
Data representation for the referee. Keeps track of the current game,
the list of players in the order they play, and kicked players.
Kicked players are those who have returned invalid moves to referee.
A Referee can be reused to run multiple games sequentially, the
manager can call Referee.reset_game() to reinitialize this referee for reuse.

A GameResult is a Dictionary with keys "state", "winners", "losers", "kicked_players", where:
    - "state" is a JSON representation of the terminal state.
    - "winners" is [List-of PlayerInterface]
    - "losers" is a [List-of PlayerInterface]
    - "kicked_players" is a [Set PlayerInterface]
and represents the result of a single game that this referee has run.
Losers of the game are players who neither lost nor cheated/were kicked out.

A BoardConfiguration is a dictionary with keys "row", "col", and "fish", where:
    - "row" is a Natural in [2,5]
    - "column" is a Natural in [2,5]
    - "fish" is a Natural in [1,5]
The BoardConfiguration describes the board dimensions and the default number of fish
on each tile.  
"""
class Referee:

    default_board_config = {"row": 4, "col": 3, "fish": 3}

    #TODO: notify players of game start and game end (alert_players does game end)

    def __init__(self, board_config=default_board_config):
        """
        Constructor for a Referee who supervises one game. 

        __board_config: BoardConfiguration        a python dictionary that describes how a board should be created
        __players: {Color : PlayerInterface}      Mapping of player's Color to the external player object
        __kicked_players: [Set PlayerInterface]   Players who have cheated, and cannot play anymore
        __game: Game                              Current Game, initialized to GameSetup
        """
        self.__board_config = board_config
        self.__players = {}
        self.__kicked_players = set()
        self.__game = GameSetup()

    def play_game(self, players):
        """
        Controls game mechanics and runs the game.

        [List-of PlayerInterface] -> GameResult
        """
        self.initialize_game(players)
        self.run_game()
        game_result = self.__get_game_result()
        # TODO catch exceptions or timeout when alerting players, delete winners from winners if they do not respond
        self.alert_players(game_result)
        return game_result

    def initialize_game(self, players):
        """
        Start the game. Initializes the game board, the game state,
        and the resulting game tree with the parameters.
        The resulting GameTree is ready to play.

        1. Takes care of what kind of Board to make (does it have holes, number of fish, etc),
        and makes sure that the board is big enough for the number of players and their penguins
        2. Calls on Players to place their penguins

        EFFECT: Sets the current Game to be the GameTree.

        [List-of PlayerInterface] -> GameTree
        """
        if type(self.__game) is not GameSetup:
            raise ValueError("Cannot initialize game: Game already started")

        internal_players = []
        for p in range(0, len(players)):
            color = self.__assign_color_to_player(p, players[p])
            self.__players[color] = players[p]
            internal_players.append(PlayerData(color))

        board = self.__create_board()
        state = State(internal_players, board)
        self.__game = GameTree(state)
        self.__run_penguin_placement()
        self.__broadcast_current_state()
        return self.__game

    def run_game(self):
        """
        Run the game until the end.
        """
        while not self.has_game_ended():
            color = self.__game.get_current_player_color()
            current_player = self.get_player_with_color(color)
            action = current_player.choose_next_move()
            maybe_game_tree =  self.check_move_validity(action)
            if maybe_game_tree is False:
                self.__kick_player(color)
                self.__broadcast_current_state()
            else:
                self.__game = maybe_game_tree
                self.__broadcast_player_action(action)

    def check_move_validity(self, action):
        """
        Check that the given action is valid in the current state of the game tree.
        If it is valid, return the next game tree with the action applied, otherwise False.

        Action -> [Maybe Game]
        """
        if type(self.__game) is not GameTree:
            return False
        return self.__game.attempt_move(action)

    def has_game_ended(self):
        """
        Utility method to see if the game has ended.

        void -> Boolean
        """
        return self.__game.has_game_ended()

    def get_current_state(self):
        """
        Get the current state of the game to inform game observers of on-going actions.
        Returns a JSON translation of the current state, which is read-only.

        void -> JSON Object
        """
        return self.__game.state.print_json()

    def get_current_scores(self):
        """
        Get scores of players.

        void -> List of (Player, int)
        """
        player_score = []
        for p in self.__game.state.players:
            ext_p = self.get_player_with_color(p.get_color())
            player_score.append((ext_p, p.get_score()))
        return player_score

    def get_winners(self):
        """
        Get the winner(s) of the game.
        If the game has not ended and there are no winners, return False.

        void -> [Maybe List of Player]
        """
        if not self.has_game_ended():
            return False
        internal_winners =  self.__game.get_winners()
        ext_winners = []
        for p in internal_winners:
            color = p.get_color()
            maybe_player = self.get_player_with_color(color)
            if maybe_player:
                ext_winners.append(maybe_player)
        return ext_winners

    def get_player_with_color(self, color):
        """
        void -> [Maybe Player]
        """
        return self.__players.get(color, False)

    def get_players_as_colors(self):
        """
        Return a list of color keys for players who have not been kicked out of the Game.

        void -> [List-of Color]
        """
        return [color for color in self.__players if self.get_player_with_color(color) not in self.__kicked_players]

    def get_players(self):
        """
        Return a list of active players in the game (those who have not cheated or failed).

        void -> [List-of PlayerInterface]
        """
        return [self.get_player_with_color(color) for color in self.get_players_as_colors()]
    

    def alert_players(self, game_result):
        """
        Send the GameResult to the active players in the game (non-kicked players).
        """
        if type(self.__game) is GameEnded:
            for player in self.get_players():
                player.game_over(game_result)

    def reset_game(self):
        """
        Reset this referee to be reused to play another Fish game.
        Should only be called after the previous game has ended and returned game results.

        EFFECT: Reinitialize all class variables to empty.
                Reset game to GameSetup()
        """
        self.__players = {}
        self.__kicked_players = set()
        self.__game = GameSetup()

    def __get_game_result(self):
        """
        Creates the game result, which includes a JSON representation of the terminal state,
        a list of the winners, and a set of the players who were kicked from the game.

        void -> GameResult
        """
        winners = self.get_winners()
        return {"state": self.__game.get_state().print_json(), 
                "winners": winners, 
                "losers": [player for player in self.get_players() if player not in winners],
                "kicked_players": self.__kicked_players}

    def __run_penguin_placement(self):
        """
        Run as many penguin placement rounds as necessary. 
        Call on Players to place their penguins.

        EFFECT: Updates the current GameTree when penguins are placed

        void -> void
        """
        rounds = get_max_penguin_count(len(self.__players))
        for round in range(0, rounds):
            for color in self.get_players_as_colors():
                state = self.__game.get_state()
                player = self.get_player_with_color(color)
                posn = player.choose_placement(state)
                maybe_state = state.place_penguin_for_player(color, posn)
                if maybe_state is False:
                    self.__kick_player(color)
                else:
                    self.__game = GameTree(maybe_state)


    def __assign_color_to_player(self, index, ext_player):
        """
        Assigns color to player based on index. Returns color assigned.

        :index: int		Index of color
        :ext_player: PlayerInterface	Player to assign color to
        :returns: Color		Color assigned
        """
        colors = Color.get_all_colors()
        assign_color = colors[index]
        ext_player.assign_color(assign_color)
        return assign_color

    def __create_board(self):
        board = Board(self.__board_config["row"], self.__board_config["col"])
        board.create_board_without_holes(self.__board_config["fish"])
        return board

    def __broadcast_player_action(self, action):
        """
        Update players who have not been kicked on ongoing game actions.
        """
        for player in self.get_players():
            player.update_with_action(action)

    def __broadcast_current_state(self):
        """
        Update players with new state. Called when a player has been kicked.
        """
        for player in self.get_players():
            player.set_state(self.__game.get_state())

    def __kick_player(self, color):
        """
        Remove the current player from the game. Tell the current player to remove penguins.

        EFFECT: Adds the current player to the set of kicked players
                Reset the current Game instance to new Game with current player removed

        Color -> void
        """
        self.__kicked_players.add(self.get_player_with_color(color))
        self.__game = self.__game.remove_player(color)
