from Game import Game
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
