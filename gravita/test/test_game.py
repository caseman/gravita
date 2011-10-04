import unittest

class GameTestCase(unittest.TestCase):

    def test_init_game(self):
        from gravita.game import Game
        map = object()
        game = Game(map)
        self.assertEqual(game.players, [])
        self.assert_(game.map is map)
        self.assertEqual(game.turn, 0)
        self.assertFalse(game.in_progress)

    def test_add_player(self):
        from gravita.game import Game
        map = object()
        game = Game(map)
        self.assertEqual(game.players, [])
        p1 = MockPlayer()
        p2 = MockPlayer()
        game.add_player(p1)
        self.assertEqual(game.players, [p1])
        self.assertRaises(Exception, game.add_player, p1)
        self.assertEqual(game.players, [p1])
        game.add_player(p2)
        self.assertEqual(game.players, [p1, p2])
        self.assertRaises(Exception, game.add_player, MockPlayer())

    def test_begin_turn_before_ready(self):
        from gravita.game import Game
        map = object()
        game = Game(map)
        self.assertRaises(Exception, game.begin_turn)
        self.assertEqual(game.turn, 0)
        game.add_player(MockPlayer())
        self.assertRaises(Exception, game.begin_turn)
        self.assertEqual(game.turn, 0)

    def test_begin_turn(self):
        from gravita.game import Game
        p1, p2 = players = (MockPlayer(), MockPlayer())
        game = Game(None)
        game.add_player(p1)
        game.add_player(p2)
        self.assertEqual(p1.turn, 0)
        self.assertEqual(p2.turn, 0)
        self.assertEqual(game.turn, 0)
        self.assertFalse(game.in_progress)
        game.begin_turn()
        self.assertEqual(p1.turn, 1)
        self.assertEqual(p2.turn, 1)
        self.assertEqual(game.turn, 1)
        self.assertTrue(game.in_progress)
        game.begin_turn()
        self.assertEqual(p1.turn, 2)
        self.assertEqual(p2.turn, 2)
        self.assertEqual(game.turn, 2)
        self.assertTrue(game.in_progress)


class MockPlayer(object):
    
    def __init__(self):
        self.turn = 0

    def begin_turn(self):
        self.turn += 1


