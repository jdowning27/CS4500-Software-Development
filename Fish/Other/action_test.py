import unittest
from Fish.Common.move import Move
from Fish.Common.skip import Skip

class ActionTestCase(unittest.TestCase):
    def setUp(self):
        self.move_origin = Move((0,0), (1,0))
        self.move2_1 = Move((0,0), (2,1))
        self.move2_0 = Move((0,0), (2,0))
        self.move2_0from = Move((2,0), (1,0))
        self.move2_1from = Move((2,1), (1,0))
        self.skip_action = Skip()

    def test_break_tie_origin(self):
        # also row to
        self.assertEqual(self.move_origin.break_tie(self.move2_1), self.move_origin)
        self.assertEqual(self.move2_1.break_tie(self.move_origin), self.move_origin)

    def test_break_tie_skip(self):
        self.assertEqual(self.skip_action.break_tie(self.move2_1), self.move2_1)
        self.assertEqual(self.move2_1.break_tie(self.skip_action), self.move2_1)

    def test_break_tie_col_to(self):
        self.assertEqual(self.move2_1.break_tie(self.move2_0), self.move2_0)
        self.assertEqual(self.move2_0.break_tie(self.move2_1), self.move2_0)

    def test_break_tie_row_from(self):
        self.assertEqual(self.move2_0from.break_tie(self.move_origin), self.move_origin)
        self.assertEqual(self.move_origin.break_tie(self.move2_0from), self.move_origin)

    def test_break_tie_col_from(self):
        self.assertEqual(self.move2_1from.break_tie(self.move2_0from), self.move2_0from)
        self.assertEqual(self.move2_0from.break_tie(self.move2_1from), self.move2_0from)

    def test_break_tie_equal(self):
        move_copy = Move((2,0), (1, 0))
        self.assertEqual(self.move2_0from.break_tie(move_copy), self.move2_0from)
        self.assertEqual(move_copy.break_tie(self.move2_0from), move_copy)


        
