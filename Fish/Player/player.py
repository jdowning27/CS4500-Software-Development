import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

from player_interface import PlayerInterface
from strategy import Strategy

class Player(PlayerInterface):

    def __init__(self, age, look_ahead=3):
        self.__age = age
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

    def get_age(self):
        return self.__age

    def get_color(self):
        return self.__color

    def get_penguins(self):
        return self.__penguins

    def get_fish(self):
        return self.__fish
