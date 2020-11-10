from game import Game
"""
Represents a game that has not started yet.
"""
class GameSetup(Game):

    def has_game_ended(self):
        return False

    def get_winners(self):
        return False

    def copy(self):
        return GameSetup()
