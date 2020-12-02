import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from Admin.referee import Referee

class ExtendedReferee(Referee):

    def _Referee__assign_player_colors(self, players):
        internal_players = super()._Referee__assign_player_colors(players)
        for player in super().get_players():
            colors_in_play = super().get_players_as_colors()
            colors_in_play.remove(player.get_color())
            player.play_with(colors_in_play)

        return internal_players