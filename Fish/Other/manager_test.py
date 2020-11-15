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
from unittest.mock import MagicMock

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
    
        
    

