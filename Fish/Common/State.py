
"""
TODO
creating a state for a certain number of players;

place an avatar on behalf of a player;

move an existing avatar from one spot to another on behalf of the player;

determine whether any player can move an avatar; and

rendering the state graphically.

A game state represents the current state of a game: 
the state of the board, 
the current placements of the penguins, 
knowledge about the players, and 
the order in which they play.

"""
"""
Represents the current game state, including:
    - the state of the board
    - the current placements of the penguins
    - knowledge about the players
    - the order in which the players take turns
"""

from tkinter import *
from Constants import MAX_FISH, GUI_UNIT

master = Tk()

class State:

    def __init__(self, players, board):
        """
        Constructor for State which constructs a game state
        with the given number of players

        :players: array         An array of Players in this game
        :board: Board           The Fish game board in this state
        """
        self.players = players
        self.board = board

    def place_penguin_for_player(self, player_color, posn):
        """
        Place a penguin at posn (row, col) for the give player if the 
        tile exists, and it is available. If a Player does not exist
        with the given Color, print a message and ignore the instruction

        :player_color: Color        The color of the Player to get
        :posn: tuple                The (row, col) position to place the penguin
        """
        player = self.get_player(player_color)
        if not player:
            print("No player with color {} found".format(player_color))
        elif not self.is_tile_available(posn):
            print("Cannot place penguin at {}".format(posn))
        else:
            player.add_penguin(posn)

    def move_penguin(self, from_posn, to_posn):
        player = self.get_player_from_penguin(from_posn)
        if self.valid_move(from_posn, to_posn) and player:
            player.move_penguin(from_posn, to_posn)
        else:
            print("Not valid move")


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




        

