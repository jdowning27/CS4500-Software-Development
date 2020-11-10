import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

import unittest
from color import *
from player_data import PlayerData

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player1 = PlayerData(Color.RED, 5)
        self.player2 = PlayerData(Color.WHITE, 10)
    
    def test_get_penguins(self):
        self.assertEqual(self.player1.get_penguins(), [])
        self.player1.add_penguin((0,0))
        self.assertEqual(self.player1.get_penguins(), [(0,0)])
    
    def test_copy(self):
        new_player = self.player1.copy()
        self.assertEqual(self.player1.get_age(), new_player.get_age())
        self.assertEqual(self.player1.get_color(), new_player.get_color())
        self.assertEqual(self.player1.get_penguins(), new_player.get_penguins())
        self.assertFalse(self.player1 is new_player)

    def test_add_penguin(self):
        self.player1.add_penguin((0,0))
        self.player1.add_penguin((1,0))
        self.assertEqual(self.player1.get_penguins(), [(0,0), (1,0)])

    def get_color(self):
        self.assertEqual(self.player1.get_color(), Color.RED)
        self.assertEqual(self.player2.get_color(), Color.WHITE)

    def get_age(self):
        self.assertEqual(self.player1.get_age(), 5)
        self.assertEqual(self.player2.get_age(), 10)

    def move_penguin_success(self):
        self.player1.add_penguin((0,0))
        self.assertEqual(self.player1.get_penguins(), [(0,0)])
        self.player1.move_penguin((0,0), (3,0))
        self.assertEqual(self.player1.get_penguins(), [(3,0)])
    
    def move_penguin_no_penguin(self):
        self.player1.add_penguin((0,0))
        self.assertEqual(self.player1.get_penguins(), [(0,0)])
        self.player1.move_penguin((3,1), (3,0))
        self.assertEqual(self.player1.get_penguins(), [(0,0)])

