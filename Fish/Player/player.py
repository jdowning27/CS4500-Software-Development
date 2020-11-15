import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

from player_interface import PlayerInterface
from strategy import Strategy
from game_setup import GameSetup
from game_tree import GameTree
from game_ended import GameEnded

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

        __color: Color                      Assigned by referee, one of red, white, brown, or black
        __strategy: Strategy                Strategy class to use when making decisions
        __look_ahead: PositiveInteger       Depth of turns to look ahead in game tree, default = 3
        __fish: Natural                     Player's current score                   
        """
        self.__color = None
        self.__strategy = Strategy()
        self.__look_ahead = look_ahead
        self.__game = GameSetup()

    def set_state(self, state):
        if state.any_remaining_moves():
            self.__game = GameTree(state)
        else:
            self.__game = GameEnded(state)

    def choose_next_move(self):
        return self.__strategy.choose_action_minimax(self.__game, self.__look_ahead)

    def choose_placement(self, state):
        posn = self.__strategy.place_penguin_across(state)
        return posn

    def assign_color(self, player_color):
        self.__color = player_color

    def update_with_action(self, action):
        self.__game = self.__game.attempt_move(action)

    def game_over(self, game_result):
        print("Player received game over")

    def get_color(self):
        return self.__color

    def tournament_start(self):
        return True

    def tournament_end(self, result):
        return True