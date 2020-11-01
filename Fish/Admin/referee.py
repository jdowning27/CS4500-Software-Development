from player import Player as ExtPlayer
from Player import Player as IntPlayer
from Color import Color
from Board import Board
from State import State
from game_tree import GameTree
"""
Data representation for the referee. Keeps track of the current game,
the list of players in the order they play, and kicked players.
Kicked players have broken the rules.
"""
class Referee:

    def __init__(self):
        self.__players = []
        self.__kicked_players = {}
        self.__game = GameSetup()
        self.__history = []

    def initialize_game(self, players):
        """
        Start the game. Initializes the game board, the game state,
        and the resulting game tree with the parameters.

        1. Takes care of what kind of Board to make (does it have holes, number of fish, etc),
        and makes sure that the board is big enough for the number of players and their penguins

        2. Calls on Players to place their penguins

        The resulting GameTree is ready to play.
        Updates the current Game to be the Game Tree.

        [Listof Player] -> GameTree
        """
        if type(self.__game) is not GameSetup:
            raise ValueError("Cannot initialize game: Game already started")
        self.__players = players
        internal_players = []
        for p in range(0, len(self.__players)):
            color = self.__assign_color_to_player(p, self.__players[p])
            internal_players.append(IntPlayer(color))

        board = self.__create_board()
        state = State(internal_players, board)
        rounds = 6 - len(self.__players)
        for round in range(0, rounds):
            for p in self.__players:
                posn = p.place_penguin(state)
                state = state.place_penguin_for_player(p.get_color(), posn)
        self.__game = GameTree(state)
        return self.__game

    def __assign_color_to_player(self, index, ext_player):
        """
        Assigns color to player based on index. Returns color assigned.

        :index: int		Index of color
        :ext_player: Player	Player to assign color to
        :returns: Color		Color assigned
        """
        colors = [Color.RED, Color.WHITE, Color.BROWN, Color.BLACK]
        assign_color = colors[index]
        ext_player.assign_color(assign_color)
        return assign_color

    def __create_board(self):
        board = Board(4, 3)
        board.create_board_without_holes(3)
        return board

    def check_move_validity(self, action):
        """
        Check that the given action is valid in the current state of the game tree.
        If it is valid, return the next game tree with the action applied, otherwise False.

        Action -> [Maybe GameTree]
        """
        if type(self.__game) is not GameTree:
            return False
        return self.__game.attempt_move(action)

    def has_game_ended(self):
        """
        Utility method to see if the game has ended.

        void -> Boolean
        """
        if self.__game.has_game_ended():
            self.__game = GameEnded()
            return True
        return False

    def get_current_state(self):
        """
        Get the current state of the game to inform game observers of on-going actions.
        Returns a JSON translation of the current state, which is read-only.

        void -> JSON Object
        """
        return self.__game.state.print_json()

    def get_curr_scores(self):
        """
        Get scores of players.

        void -> {Player: int}
        """
        player_score = {}
        for p in self.__game.state.players:
            player_score[p] = p.get_score()
        return player_score

    def get_winners(self):
        """
        Get the winner(s) of the game.
        If the game has not ended and there are no winners, return False.

        void -> [Maybe List of Player]
        """
        if not self.has_game_ended():
            return False
        return self.__game.get_winner()

    def get_history(self):
        """
        Get the game history. The tournament manager may use this in its own tournament statistics.
        Returns a list of Player to Action mappings.

        void -> [Listof (Player, Action)]
        """
        return self.__history

    def play_game(self, players):
        """
        Controls game mechanics and runs the game.

        :players: List of Players	External Player representations
        :returns: GameEnded		Final Game
        """
        self.initialize_game(players)
        while not self.has_game_ended():
            current_player = self.__players[0]
            action = current_player.choose_next_move(self.__game.copy())
            maybe_game_tree =  self.check_move_validity(action)
            if not maybe_game_tree:
                self.__kicked_players.add(current_player)
                current_player.remove_penguins()
                self.__players.pop(0)
                self.__game = self.__game.remove_current_player()
            else:
                self.__history.append(self.__game.get_current_player_color(), action)
                self.__game = maybe_game_tree
                from_posn = action.get_from_posn()
                current_player.move_penguin(from_posn, action.get_to_posn(), self.__game.state.get_fish_at(from_posn))
                self.next_turn()
        return self.__game

    def next_turn(self):
        """
        Shifts the player list so it is the next player's turn.

        :returns: void
        """
        self.__players = self.__players[1:] + self.__players[:1]
