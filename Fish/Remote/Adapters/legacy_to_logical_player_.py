from Fish.Common.player_interface import PlayerInterface
from Fish.Common.game_tree import GameTree
from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface

class LegacyToLogicalPlayer(PlayerInterface):
    
    def __init__(self, logical_player):

        self.__is_valid_logical_player_type(logical_player)

        self.__logical_player = logical_player
        self.__state = None
        self.__color = None

    def __is_valid_logical_player_type(self, logical_player):
        if not issubclass(logical_player, LogicalPlayerInterface):
            raise ValueError("logical_player must a subclass of LogicalPlayerInterface")


    def set_state(self, state):
        self.__state = state

    def choose_next_move(self):
        self.__logical_player.tt(self.__state, [])
    
    def choose_placement(self, state):
        self.__logical_player.setup(state)

    def assign_color(self, player_color):
        self.__color = player_color
        self.__logical_player.play_as(player_color)

    def play_with(self, player_colors):
        self.__logical_player.play_with(player_colors)

    def game_over(self, game_result):
        pass

    def update_with_action(self, action):
        tree = GameTree(self.__state)
        self.__state = action.apply_move(tree)

    def get_color(self):
        return self.__color

    def tournament_start(self):
        self.__logical_player.start(True)

    def tournament_end(self, result):
        self.__logical_player.end(result)