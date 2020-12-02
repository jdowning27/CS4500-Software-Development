import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from Admin.referee import Referee

class ExtendedReferee(Referee):

    def _Referee__assign_player_colors(self, players):
        """
        assigns the player colors to all players in this game. it also informs
        players about the other colors that are playing in this game
        Effect: calls the super().__assign_player_colors method, and then calls 
            player.play_with() for all players in the game with the colors of their opponents

        [List-of PlayerInterface] -> Void
        """
        internal_players = super()._Referee__assign_player_colors(players)
        for player in super().get_players():
            colors_in_play = super().get_players_as_colors()
            colors_in_play.remove(player.get_color())
            player.play_with(colors_in_play)

        return internal_players