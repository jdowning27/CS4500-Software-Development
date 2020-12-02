from copy import copy
from Fish.Admin.referee import Referee
from Fish.Common.util import safe_call


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
        for player_data in copy(internal_players):
            colors_in_play = super().get_players_as_colors()
            color = player_data.get_color()
            colors_in_play.remove(color)
            if safe_call(self._Referee__timeout,
                         self.get_player_with_color(color).play_with,
                         [colors_in_play]) is False:
                self._Referee__kick_player(color)
                internal_players.remove(player_data)

        return internal_players
