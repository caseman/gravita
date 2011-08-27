import unittest

class GameTestCase(unittest.TestCase):

    def test_init_game(self):
        from gravita.game import Game
        map = object()
        players = ('foo', 'bar')
        game = Game(players, map)
        self.assertEqual(game.players, players)
        self.assert_(game.map is map, game.map)

