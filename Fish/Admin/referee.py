from player import Player as ExtPlayer
from Player import Player as IntPlayer
from color import Color
from board import Board
from state import State
from skip import Skip
from game_tree import GameTree
from game_setup import GameSetup
from game_ended import GameEnded
"""
Data representation for the referee. Keeps track of the current game,
the list of players in the order they play, and kicked players.
Kicked players are those who have returned invalid moves to referee.
"""
class Referee:

    def __init__(self):
        """
        Constructor for a Referee who supervises one game. 

        __players: [List-of Player]      External players who play the game, in the order in which they play
        __kicked_players: [Set Player]   Players who have cheated, and cannot play anymore
        __game: Game                     Current Game, initialized to GameSetup
        __history: [List-of (Player, Action)]  History of all game actions mapped to Player
        """
        self.__players = []
        self.__kicked_players = set()
        self.__game = GameSetup()
        self.__history = []

    def play_game(self, players):
        """
        Controls game mechanics and runs the game.

        :players: List of Players       External Player representations
        :returns: GameEnded             Final Game
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
                self.__history.append((self.__game.get_current_player_color(), action))
                self.__game = maybe_game_tree
                if type(action) is not Skip:
                    from_posn = action.get_from_posn()
                    current_player.move_penguin(from_posn, action.get_to_posn(), self.__game.state.get_fish_at(from_posn))
                self.next_turn()
        self.alert_players()
        return self.__game


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
        if type(self.__game) is GameEnded:
            return True
        elif type(self.__game) is GameTree and  self.__game.has_game_ended():
            self.__game = GameEnded(self.__game.state)
            return True
        return False

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

    def get_history(self):
        """
        Get the game history. The tournament manager may use this in its own tournament statistics.
        Returns a list of Player to Action mappings.

        void -> [Listof (Player, Action)]
        """
        return self.__history

    def alert_players(self):
        """
        Alert each player that the game is over and tell them who the winner(s) are.
        """
        if type(self.__game) is GameEnded:
            for p in self.__players:
                p.game_over(self.__game.get_state().print_json(), self.get_winners())

    def next_turn(self):
        """
        Shifts the player list so it is the next player's turn.

        :returns: void
        """
        self.__players = self.__players[1:] + self.__players[:1]

    def get_player_with_color(self, color):
        for p in self.__players:
            if p.get_color() == color:
                return p
        return False

    def get_players(self):
        return self.__players
