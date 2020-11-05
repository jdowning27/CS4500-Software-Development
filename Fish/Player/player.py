import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

from player_interface import PlayerInterface
from strategy import Strategy

"""
Implementation of a player for Fish game.
This player chooses to place penguins and make moves according to the following strategy:
    - Places penguins across rows, see purpose in strategy.py `place_penguins_across`
    - Moves according to maximal gain strategy, see purpose in strategy.py `choose_action_minimax`
Keeps track of their penguins, a color (assigned by the Referee), its strategy,
depth to look ahead in the game tree, and number of fish (the score)
"""
class Player(PlayerInterface):

    def __init__(self, look_ahead=3):
        """
        Constructor for a player for Fish game.

        __penguins: [Set (int, int)]        Set of posn (row, col) of each penguin
        __color: Color                      Assigned by referee, one of red, white, brown, or black
        __strategy: Strategy                Strategy class to use when making decisions
        __look_ahead: PositiveInteger       Depth of turns to look ahead in game tree, default = 3
        __fish: Natural                     Player's current score                   
        """
        self.__penguins = set()
        self.__color = None
        self.__strategy = Strategy()
        self.__look_ahead = look_ahead
        self.__fish = 0

    def choose_next_move(self, tree):
        return self.__strategy.choose_action_minimax(tree, self.__look_ahead)

    def place_penguin(self, state):
        posn = self.__strategy.place_penguin_across(state)
        self.__penguins.add(posn)
        return posn

    def assign_color(self, player_color):
        if self.__color is None:
            self.__color = player_color

    def move_penguin(self, from_posn, to_posn, fish):
        if from_posn in self.__penguins:
            self.__penguins.remove(from_posn)
            self.__penguins.add(to_posn)
            self.__fish += fish
        else:
            print("Illegal Move: This player does not have penguin at", from_posn )

    def remove_penguins(self):
        # Set to None so player cannot add again
        self.__penguins = None

    def game_over(self, state, winners):
        print("Player received game over")

    def get_color(self):
        return self.__color

    def get_penguins(self):
        return self.__penguins

    def get_fish(self):
        return self.__fish
