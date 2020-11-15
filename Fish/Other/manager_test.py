import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Player'
sys.path.append(os_path)
os_path = os.path.dirname(os.getcwd()) + '/Fish/Admin'
sys.path.append(os_path)
from player import Player
from manager import Manager
from move import Move

import unittest
from unittest.mock import patch, MagicMock

class RefereeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.player1 = Player(1)
        self.player2 = Player(1)
        self.player3 = Player(2)
        self.player4 = Player(1)
        self.player5 = Player(1)
        self.player6 = Player(2)
        self.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6]

        self.manager = Manager()

    ## TESTING RUN TOURNAMENT ################################################################

    def test_run_tournament(self):
        winners = self.manager.run_tournament(self.players)
        self.assertEqual(winners, [self.player1, self.player4, self.player5])

    def test_run_tournament_failing_player_start(self):
        self.player5.tournament_start = MagicMock(return_value=False)
        winners = self.manager.run_tournament(self.players)
        
        self.assertEqual(winners, [self.player1, self.player3, self.player4])

    def test_run_tournament_failing_player_winner(self):
        self.player5.tournament_end = MagicMock(return_value=False)
        winners = self.manager.run_tournament(self.players)
        self.assertEqual(winners, [self.player1, self.player4])

    def test_run_tournament_everyone_fails(self):
        self.player1.choose_next_move = MagicMock(return_value=Move((0,0), (1, 1))) # illegal move
        self.player2.choose_placement = MagicMock(return_value=(0,0)) # penguin already there
        self.player3.choose_placement = MagicMock(return_value=(-1, 0))
        self.player4.choose_next_move = MagicMock(return_value=Move((0,0), (2, 0))) # no penguin to move
        self.player5.choose_next_move = MagicMock(return_value=Move((0,0), (1, 1))) 
        self.player6.choose_next_move = MagicMock(return_value=Move((0,0), (1, 1)))

        winners = self.manager.run_tournament(self.players)
        self.assertEqual(winners, [])

    ## TESTING UPDATE BRACKET ################################################################

    def test_update_bracket(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)
        round_result = {
            "winners": { self.player1, self.player2 },
            "losers": {self.player3, self.player4 },
            "kicked_players": { self.player5, self.player6 },
            "games_played": 2
        }
        self.assertEqual(self.manager._Manager__queue, self.players)
        self.assertEqual(self.manager._Manager__active_players, set(self.players))
        self.assertEqual(self.manager._Manager__previous_winners, set())
        self.assertEqual(self.manager._Manager__kicked_players, set())
        self.assertEqual(self.manager._Manager__games_in_previous_round, 0)

        self.manager._Manager__update_bracket(round_result)
        self.assertEqual(self.manager._Manager__queue, [self.player1, self.player2])
        self.assertEqual(self.manager._Manager__active_players, {self.player1, self.player2, self.player3, self.player4})
        self.assertEqual(self.manager._Manager__previous_winners, {self.player1, self.player2, self.player3, self.player4})
        self.assertEqual(self.manager._Manager__kicked_players, {self.player5, self.player6})
        self.assertEqual(self.manager._Manager__games_in_previous_round, 2)

    ## TESTING KICK PLAYERS ------------------------------------------------------------

    def test_kick_players(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)

        bad_players = {self.player6, self.player1}
        self.manager._Manager__kick_players(bad_players)
        self.assertEqual(self.manager._Manager__queue, self.players[1:5])
        self.assertEqual(self.manager._Manager__active_players, set(self.players[1:5]))
        self.assertEqual(self.manager._Manager__kicked_players, bad_players)

    def test_kick_players_no_bad_players(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)

        bad_players = set()
        self.manager._Manager__kick_players(bad_players)
        self.assertEqual(self.manager._Manager__queue, self.players)
        self.assertEqual(self.manager._Manager__active_players, set(self.players))
        self.assertEqual(self.manager._Manager__kicked_players, bad_players)
    
    ## TESTING RUN ROUNDS ################################################################-

    def test_run_round(self):
        match_players = [
            self.players[0:4],
            self.players[4:6]
        ]
        expected = {
            "winners": {self.player1, self.player3, self.player4, self.player5},
            "losers": {self.player2, self.player6},
            "kicked_players": set(),
            "games_played": 2
        }
        round_result = self.manager._Manager__run_round(match_players)
        self.assertEqual(round_result, expected)

    def test_run_round_failing_player(self):
        self.player1.choose_next_move = MagicMock(return_value=Move((0,0), (4, 4))) # runs into another penguin
        match_players = [
            self.players[0:4],
            self.players[4:6]
        ]
        expected = {
            "winners": {self.player3, self.player5},
            "losers": {self.player2, self.player4, self.player6},
            "kicked_players": {self.player1},
            "games_played": 2
        }
        round_result = self.manager._Manager__run_round(match_players)
        self.assertEqual(round_result, expected)

    ## TESTING MAKE ROUNDS ################################################################

    def test_make_rounds(self):
        self.manager._Manager__queue = self.players

        expected = [
            self.players[0:4],
            self.players[4:6]
        ]
        match_players = self.manager._Manager__make_rounds()
        self.assertEqual(match_players, expected)

    def test_make_rounds_no_players(self):
        self.assertRaisesRegex(ValueError, "Not enough players to run another round.", self.manager._Manager__make_rounds)

    def test_make_rounds_backtracking(self):
        self.manager._Manager__queue = self.players[0:5]
        expected = [
            self.players[0:3],
            self.players[3:5]
        ]
        match_players = self.manager._Manager__make_rounds()
        self.assertEqual(match_players, expected)
    
    def test_make_rounds_min_players(self):
        self.manager._Manager__queue = self.players[0:2]
        expected = [
            self.players[0:2]
        ]
        match_players = self.manager._Manager__make_rounds()
        self.assertEqual(match_players, expected)

    ## TESTING BALANCE GAME ################################################################
    
    def test_balance_games(self):
        match_players = [
            self.players[0:4],
            self.players[4:5]
        ]
        expected = [
            self.players[0:3],
            self.players[3:5]
        ]
        balanced = self.manager._Manager__balance_games(match_players)
        self.assertEqual(balanced, expected)

    def test_balance_games_already_balanced(self):
        match_players = [
            self.players[0:4],
            self.players[4:6]
        ]
        self.assertEqual(self.manager._Manager__balance_games(match_players), match_players)
    
    def test_balance_games_one_game(self):
        match_players = [
            self.players[0:2]
        ]
        self.assertEqual(self.manager._Manager__balance_games(match_players), match_players)
    
    ## TESTING IS TOURNAMENT OVER ###########################################################

    def test_is_tournament_over_false(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__previous_winners = set()
        self.manager._Manager__games_in_previous_round = 2
        self.assertFalse(self.manager._Manager__is_tournament_over())

    def test_is_tournament_over_same_winners(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__previous_winners = set(self.players)
        self.assertTrue(self.manager._Manager__is_tournament_over())

    def test_is_tournament_over_too_few_players(self):
        self.manager._Manager__queue = self.players[0:1]
        self.assertTrue(self.manager._Manager__is_tournament_over())

    def test_is_tournament_over_one_game_round(self):
        self.manager._Manager__queue = self.players[0:3]
        self.manager._Manager__previous_winners = set(self.players)
        self.manager._Manager__games_in_previous_round = 1
        self.assertTrue(self.manager._Manager__is_tournament_over())


    ## TESTING BROADCAST TOURNAMENT START ###################################################

    def test_broadcast_tournament_start(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)

        self.player1.tournament_start = MagicMock(return_value=True)
        self.manager._Manager__broadcast_tournament_start() 
        self.player1.tournament_start.assert_called()
        self.assertEqual(self.manager._Manager__queue, self.players)
        self.assertEqual(self.manager._Manager__active_players, set(self.players))

    def test_broadcast_tournament_start_player_bad_response(self):
        self.player1.tournament_start = MagicMock(return_value=False)
        self.player2.tournament_start = MagicMock(return_value="True")
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)
        self.manager._Manager__broadcast_tournament_start() 
        self.assertEqual(self.manager._Manager__queue, self.players[2:6])
        self.assertEqual(self.manager._Manager__active_players, set(self.players[2:6]))


    ## TESTING BROADCAST TOURNAMENT END #####################################################

    def test_broadcast_tournament_end_good_players(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)
        round_result = {
            "winners": {self.player1, self.player4, self.player5},
            "losers": {self.player2, self.player6},
            "kicked_players": {self.player3},
            "games_played": 1
        }
        self.manager._Manager__update_bracket(round_result)
        self.player1.tournament_end = MagicMock(return_value=True)
        self.player2.tournament_end = MagicMock(return_value=True)
        self.manager._Manager__broadcast_tournament_end() 
        self.player1.tournament_end.assert_called_with(True)
        self.player2.tournament_end.assert_called_with(False)

    def test_broadcast_tournament_end_bad_winner(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)
        round_result = {
            "winners": {self.player1, self.player4, self.player5},
            "losers": {self.player2, self.player6},
            "kicked_players": {self.player3},
            "games_played": 1
        }
        self.manager._Manager__update_bracket(round_result)
        self.player4.tournament_end = MagicMock(return_value=False)
        self.manager._Manager__broadcast_tournament_end()
        self.player4.tournament_end.assert_called_with(True)
        self.assertTrue(self.player4 in self.manager._Manager__kicked_players)

    def test_broadcast_tournament_end_kicked_player_not_called(self):
        self.manager._Manager__queue = self.players
        self.manager._Manager__active_players = set(self.players)
        round_result = {
            "winners": {self.player1, self.player4, self.player5},
            "losers": {self.player2, self.player6},
            "kicked_players": {self.player3},
            "games_played": 1
        }
        self.manager._Manager__update_bracket(round_result)
        self.player3.tournament_end = MagicMock(return_value=True)
        self.manager._Manager__broadcast_tournament_end()
        self.player3.tournament_end.assert_not_called()

    ## TESTING GET TOURNAMENT RESULT ########################################################

    def test_get_tournament_result(self):
        self.manager._Manager__queue = self.players
        self.assertEqual(self.manager._Manager__get_tournament_result(), self.players)


