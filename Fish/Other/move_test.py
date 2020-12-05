import unittest
from Fish.Common.move import Move


class PlayerTestCase(unittest.TestCase):

    def test_from_json(self):
        jsons = [
            [[0, 0], [1, 0]],
            [[2, 0], [3, 0]],
            [[3, 1], [1, 2]],
            [[0, 0], [6, 3]]
        ]
        moves = [
            Move((0, 0), (1, 0)),
            Move((2, 0), (3, 0)),
            Move((3, 1), (1, 2)),
            Move((0, 0), (6, 3))
        ]
        for json, move in zip(jsons, moves):
            m = Move.from_json(json)
            self.assertEqual(move.print_json(), m.print_json())
            self.assertEqual(move, m)
