from tkinter import *
from constants import MAX_FISH, GUI_UNIT, MIN_PLAYERS, MAX_PLAYERS
from move import Move
from skip import Skip

master = Tk()


"""
Represents a snapshot of the state of the game, which includes:
    - the state of the board, using Board class
    - a sorted list of PlayerData, in order of turns
        - PlayerData keeps track of its penguins, represented as a list of (row, col) tuples, score, and color
"""
class State:

    def __init__(self, players, board):
        """
        Constructor for State which constructs a game state
        with the given number of players. 
        Must have between MIN_PLAYERS and MAX_PLAYERS.
        Player's Colors must be unique.

        :players: PlayerData[]  An array of Players in this game, assume sorted by age
        :board: Board           The Fish game board in this state
        """
        if len(players) < MIN_PLAYERS or len(players) > MAX_PLAYERS:
            raise ValueError("Invalid number of players")
        seen_colors = []
        for player in players:
            if player.get_color() in seen_colors:
                raise ValueError("Players cannot have duplicate colors")
            seen_colors.append(player.get_color())
        
        self.players = players
        self.board = board

    def __eq__(self, other):
        return type(other) is State and self.board == other.board and self.players == other.players

    def place_penguin_for_player(self, player_color, posn):
        """
        Place a penguin at posn (row, col) for the give player if the 
        tile exists, and it is available. If a Player does not exist
        with the given Color, print a message and ignore the instruction

        :player_color: Color        The color of the Player to get
        :posn: tuple                The (row, col) position to place the penguin
        :returns: maybe State		Returns a game state with the penguin added if possible
        """
        new_state = self.copy()
        player = new_state.get_player(player_color)
        if not player:
            print("No player with color {} found".format(player_color))
            return False
        elif not self.is_tile_available(posn):
            print("Cannot place penguin at {}".format(posn))
            return False
        else:
            player.add_penguin(posn)
            return new_state

    def copy(self):
        """
        Creates a deep copy of the game state.

        :returns: State		Copy of this game state
        """
        players = []
        for player in self.players:
            players.append(player.copy())
        board = self.board.copy()
        return State(players, board)


    def move_penguin(self, from_posn, to_posn):
        """
        Move the penguin for the current player if it is a vaid move.
        It is a valid move if there is a penguin on the from posn and the to_posn is reachable
        The penguin on the from posn needs to be a penguin of the current player

        :from_posn: tuple	(row, col) of tile where penguin to be moved is
        :to_posn: tuple		(row, col) of tile to move the penguin to
        :returns: maybe State   A game state with the penguin moved if possible
        """
        player = self.get_player_from_penguin(from_posn)
        if self.valid_move(from_posn, to_posn) and player is self.players[0]:
            new_state = self.copy()
            fish = self.board.tiles[from_posn[1]][from_posn[0]].get_fish()
            new_state.board.remove_tile(*from_posn)
            new_state.players[0].move_penguin(from_posn, to_posn)
            new_state.players[0].add_to_score(fish)
            new_state.set_next_players_turn()
            return new_state
        else:
            print("Not a valid move")
            return False


    def valid_move(self, from_posn, to_posn):
        """
        Is this a valid move for a penguin? Check if from_posn contains
        a penguin, and also check if to_posn is available to move to from the
        origin. 

        :from_posn: tuple       The (row, col) origin position
        :to_posn: tuple         The (row, col) position to move to
        :returns: bool          True if the move is valid
        """
        return from_posn in self.get_all_penguins() and \
            self.is_tile_available(to_posn) and \
            to_posn in self.board.get_all_reachable_posn(*from_posn)

    def any_remaining_moves(self):
        """
        Determines if any Player can move a penguin on the board

        :returns: bool      True if any Player can make a move
        """
        for penguin in self.get_all_penguins():
            for reachable in self.board.get_all_reachable_posn(*penguin):
                if self.valid_move(penguin, reachable):
                    return True
        return False


    def get_player_from_penguin(self, penguin):
        """
        Get the Player object that has the given penguin.
        If no such Player exists, return False meaning a Player was not found.

        :penguin: tuple     The (row, col) location of the penguin
        """
        for player in self.players:
            if penguin in player.get_penguins():
                return player
        return False

    def get_all_penguins(self):
        """
        Returns a list of tuples of all the positions of all penguins
        on the board.

        :returns: array     The list of penguin positions
        """
        all_penguins = []
        for player in self.players:
            all_penguins.extend(player.get_penguins())
        return all_penguins

    def get_player(self, player_color):
        """
        Gets Player object with the given color. If none exists,
        return False
        
        :player_color: Color            Player's color to get
        :returns: [Maybe Player]      returns a maybe Player
        """
        for player in self.players:
            if player.get_color() == player_color:
                return player
        return False 

    def is_tile_available(self, posn):
        """
        Does the given tile exist on the board, and are there no
        other penguins on the tile?

        :posn: tuple    The (row, col) position to check on the board
        :returns: bool  True if the tile is available
        """
        return self.board.tile_exists(posn) and posn not in self.get_all_penguins()

    def draw_state(self):
        """
        Draw the current game state with tiles, fish, holes in board, and penguins
        """
        w, h = self.board.get_dimensions()
        canvas = Canvas(master, width=w, height=h)
        self.board.draw_board(canvas)
        for penguin in self.get_all_penguins():
            player = self.get_player_from_penguin(penguin)
            player_color = player.get_color()
            self.board.draw_penguin(canvas, player_color.value, penguin)
        master.mainloop()

    def get_possible_moves(self):
        """
        Gets a list of all of the possible moves for the current player in this state.

        :returns: List of Action	possible actions for player
        """
        penguins = self.players[0].get_penguins()
        possible_moves = []
        for p in penguins:
            for reachable in self.board.get_all_reachable_posn(*p, self.get_all_penguins()):
                if self.valid_move(p, reachable):
                    possible_moves.append(Move(p, reachable))
        if len(possible_moves) == 0: # there are no possible moves for player
            possible_moves = [Skip()]
        return possible_moves

    def print_json(self):
        """
        Returns a json representation of the state as a json object

        :returns: Dictionary	State as json
        """
        state = {}
        players = []
        for player in self.players:
            players.append(player.print_json())
        state['players'] = players
        state['board'] = self.board.print_json()
        return state

    def get_players_score(self, player_color):
        return self.get_player(player_color).get_score()

    def get_current_player_color(self):
        return self.players[0].get_color()

    def set_next_players_turn(self):
        self.players = self.players[1:] + self.players[:1]

    def get_fish_at(self, posn):
        return self.board.tiles[posn[1]][posn[0]].get_fish()

    def remove_player(self, color):
        """
        Removes the player with given color and their penguins from the board without creating holes.
        If player with given color is not found, return the same state.

        Color -> State
        """
        new_state = self.copy()
        player = new_state.get_player(color)
        if player is not False:
            new_state.players.remove(player)
        return new_state
        
    def get_winners(self):
        max_score = 0
        winning_players = []
        for p in self.players:
            score = p.get_score()
            if score == max_score:
                winning_players.append(p)
            elif score > max_score:
                max_score = score
                winning_players = [p]
        return winning_players
                
