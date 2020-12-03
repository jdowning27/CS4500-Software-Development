from Fish.Common.player_interface import PlayerInterface
from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface


class LogicalToLegacyPlayer(LogicalPlayerInterface):
    """
    Adapts the interface LogicalPlayerInterface to an object of interface PlayerInterface.

    Class attributes:
        self.__legacy_player:   A player that implements PlayerInterface
                                to which calls will be translated.
    """

    def __init__(self, legacy_player):
        """Initializes a LogicalToLegacyPlayer that will make calls to legacy_player.

        PlayerInterface -> LogicalPlayerInterface
        """
        if not issubclass(type(legacy_player), PlayerInterface):
            raise ValueError("legacy_player must be a subclass of PlayerInterface")
        self.__legacy_player = legacy_player

    def start(self, starting):
        self.__legacy_player.tournament_start()

    def end(self, did_win):
        self.__legacy_player.tournament_end(did_win)

    def play_as(self, color):
        self.__legacy_player.assign_color(color)

    def play_with(self, colors):
        self.__legacy_player.play_with(colors)

    def setup(self, state):
        return self.__legacy_player.choose_placement(state)

    def tt(self, state, actions):
        self.__legacy_player.set_state(state)
        return self.__legacy_player.choose_next_move()
