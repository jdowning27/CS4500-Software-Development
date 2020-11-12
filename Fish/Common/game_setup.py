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

    def get_players_score(self, player_color):
        return 0
    
    def get_possible_actions(self):
        return []

    def get_current_player_color(self):
        return False