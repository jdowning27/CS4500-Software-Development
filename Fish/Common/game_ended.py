from Fish.Common.game import Game
"""
Represents a game which has ended.
"""
class GameEnded(Game):

    def __init__(self, state):
        if state.any_remaining_moves():
            raise ValueError("Game state has remaining moves. Game is not over.")
        self.__state = state

    def has_game_ended(self):
        return True

    def get_winners(self):
        return self.__state.get_winners()

    def copy(self):
        return GameEnded(self.__state.copy())

    def get_state(self):
        return self.__state

    def get_players_score(self, player_color):
        return self.__state.get_players_score(player_color)

    def get_possible_actions(self):
        return []
    
    def get_current_player_color(self):
        return False
