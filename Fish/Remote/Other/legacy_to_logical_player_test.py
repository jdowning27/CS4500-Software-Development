import unittest

from Fish.Player.player import Player
from Fish.Common.state import State
from Fish.Common.player_data import PlayerData
from Fish.Common.board import Board
from Fish.Common.color import Color
from Fish.Common.move import Move
from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface
from Fish.Remote.Adapters.legacy_to_logical_player import LegacyToLogicalPlayer

class TestExtendedReferee(unittest.TestCase):

    def setUp(self):
        self.logical_player = LogicalPlayerInterface()
        self.adapted_player = LegacyToLogicalPlayer(self.logical_player)

        self.board = Board(4, 4)
        self.players = [PlayerData(Color.RED), PlayerData(Color.WHITE), PlayerData(Color.BROWN)]
        state = State(self.players, self.board)
        state = state.place_penguin_for_player(Color.RED, (0, 0))
        state = state.place_penguin_for_player(Color.WHITE, (1, 1))
        state = state.place_penguin_for_player(Color.BROWN, (1, 3))
        self.state = state
        # R   X   X   X
        #   X   W   X   B
        # X   X   X   X
        #   X   X   X   X

    # Testing __init__ ###################################################

    def test_bad_player(self):
        self.assertRaisesRegex(
            ValueError, "logical_player must a subclass of LogicalPlayerInterface",
            LegacyToLogicalPlayer, Player())
    
    def test_good_player(self):
        adapted_player = LegacyToLogicalPlayer(self.logical_player)
        self.assertEqual(
            adapted_player._LegacyToLogicalPlayer__logical_player,
            self.logical_player)

    # Testing set_state ####################################################

    def test_set_state(self):
        self.adapted_player.set_state(self.state)
        actual = self.adapted_player_LegacyToLogicalPlayer__state
        expected = self.state.copy()
        self.assertEqual(actual, expected)

    # Testing choose_next_move #############################################
    # def test_choose_next_move(self):

    # Testing choose_placement #############################################
    # def test_choose_placement(self):

    # Testing assign_color #############################################
    def test_assign_color(self):
        self.adapted_player.play_with(Color.RED)
        self.assertEqual(self.adapted_player.get_color(), Color.RED)

    # Testing play_with #############################################
    # def test_play_with(self):

    # Testing game_over #############################################
    # def test_game_over(self):

    # Testing update_with_action #############################################
    def test_update_with_action1(self):
        action = Move((0, 0), (0, 1))
        state = self.state.move_penguin(action.get_from_posn(), action.get_to_posn())
        # 0   X   X   X
        #   R   W   X   B
        # X   X   X   X
        #   X   X   X   X
        self.adapted_player.update_with_action(action)
        self.assertEqual(state, self.adapted_player._LegacyToLogicalPlayer__state)
    
    def test_update_with_action2(self):
        action = Move((0, 0), (3, 2))
        state = self.state.move_penguin(action.get_from_posn(), action.get_to_posn())
        # 0   X   X   X
        #   X   W   X   B
        # X   X   X   X
        #   X   R   X   X
        self.adapted_player.update_with_action(action)
        self.assertEqual(state, self.adapted_player._LegacyToLogicalPlayer__state)
    
    def test_update_with_multiple_actions(self):
        action1 = Move((0, 0), (3, 2))
        action2 = Move((1, 1), (0, 2))
        state = self.state.move_penguin(action1.get_from_posn(), action1.get_to_posn())
        state = self.state.move_penguin(action2.get_from_posn(), action2.get_to_posn())
        # 0   X   W   X
        #   X   0   X   B
        # X   X   X   X
        #   X   R   X   X
        self.adapted_player.update_with_action(action1)
        self.adapted_player.update_with_action(action2)
        self.assertEqual(state, self.adapted_player._LegacyToLogicalPlayer__state)



    # Testing get_color #############################################
    # def test_get_color(self):

    # Testing tournament_start #############################################
    # def test_tournament_start(self):

    # Testing tournament_end #############################################
    # def test_tournament_end(self):