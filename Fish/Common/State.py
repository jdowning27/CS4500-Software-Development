from tkinter import *
from Constants import MAX_FISH, GUI_UNIT

master = Tk()


"""
Represents a snapshot of the state of the game, which includes:
    - the state of the board
    - the current placements of the penguins
    - knowledge about the players
    - the order in which the players take turns
"""
class State:

    def __init__(self, players, board, turn=0):
        """
        Constructor for State which constructs a game state
        with the given number of players

        :players: array         An array of Players in this game
        :board: Board           The Fish game board in this state
        :turn: int		The index of the player whose turn it is
        """
        players.sort(key=lambda p: p.get_age())
        self.players = players
        self.board = board
        self.turn = turn

    def place_penguin_for_player(self, player_color, posn):
        """
        Place a penguin at posn (row, col) for the give player if the 
        tile exists, and it is available. If a Player does not exist
        with the given Color, print a message and ignore the instruction

        :player_color: Color        The color of the Player to get
        :posn: tuple                The (row, col) position to place the penguin
        :returns: State		        Returns a game state with the penguin added if possible
        """
        new_state = self.copy()
        player = new_state.get_player(player_color)
        if not player:
            print("No player with color {} found".format(player_color))
            return self
        elif not self.is_tile_available(posn):
            print("Cannot place penguin at {}".format(posn))
            return self
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
        return State(players, board, self.turn)


    def move_penguin(self, from_posn, to_posn):
        """
        Move the penguin for the current player if it is a vaid move.
        It is a valid move if there is a penguin on the from posn and the to_posn is reachable
        The penguin on the from posn needs to be a penguin of the current player

        :from_posn: tuple	(row, col) of tile where penguin to be moved is
        :to_posn: tuple		(row, col) of tile to move the penguin to
        :returns: State     A game state with the penguin moved if possible
        """
        player = self.get_player_from_penguin(from_posn)
        if self.valid_move(from_posn, to_posn) and player is self.players[self.turn]:
            new_state = self.copy()
            new_state.board.remove_tile(*from_posn)
            new_state.players[self.turn].move_penguin(from_posn, to_posn)
            new_state.turn = (self.turn + 1) % len(self.players)
            return new_state
        else:
            print("Not valid move")
            return self


    def valid_move(self, from_posn, to_posn):
        """
        Is this a valid move for a penguin? Check if from_posn contains
        a penguin, and also check if to_posn is available to move to from the
        origin. 

        :from_posn: tuple       The (row, col) origin position
        :to_posn: tuple         The (row, col) position to move to
        :returns: bool          True if the move is valid
        """
        row, col = from_posn
        return from_posn in self.get_all_penguins() and \
            self.is_tile_available(to_posn) and \
            to_posn in self.board.get_all_reachable_posn(row, col)

    def any_remaining_moves(self):
        """
        Determines if any Player can move a penguin on the board

        :returns: bool      True if any Player can make a move
        """
        for player in self.players:
            for penguin in player.get_penguins():
                row, col = penguin
                for reachable in self.board.get_all_reachable_posn(row, col):
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
        :returns: Player or False       returns a maybe Player
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




        

