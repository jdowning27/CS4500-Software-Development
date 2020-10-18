import unittest
from GameTree import *

class GameTreeTestCase(unittest.TestCase):

    def setUp(self):
        self.board_full = Board(4, 3)
        self.board_full.create_board_without_holes(4)
        self.board_holes = Board(4, 3)
        self.board_holes.create_board_with_holes([(0,0), (1,1)], 3)

        self.player1 = Player(Color.RED, 5)
        self.player2 = Player(Color.WHITE, 10)
        self.players = [self.player1, self.player2]

        self.state_full = State(self.players, self.board_full)
        self.state_holes = State(self.players, self.board_holes)

        self.game_tree = GameTree(state_full)

    def test_attempt_move(self):
        
