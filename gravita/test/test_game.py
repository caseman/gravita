import unittest

class GameTestCase(unittest.TestCase):

    def test_init_game(self):
        from gravita.game import Game
        players = ('foo', 'bar')
        map = object()
        game = Game(players, map)
        self.assertEqual(game.players, players)
        self.assert_(game.map is map)
        self.assertEqual(game.turn, 0)

    def test_begin_turn(self):
        from gravita.game import Game
        p1, p2 = players = (MockPlayer(), MockPlayer())
        game = Game(players, None)
        self.assertEqual(p1.turn, 0)
        self.assertEqual(p2.turn, 0)
        game.begin_turn()
        self.assertEqual(p1.turn, 1)
        self.assertEqual(p2.turn, 1)
        game.begin_turn()
        self.assertEqual(p1.turn, 2)
        self.assertEqual(p2.turn, 2)


class MockPlayer(object):
    
    def __init__(self):
        self.turn = 0

    def begin_turn(self):
        self.turn += 1


