import unittest

class GameTestCase(unittest.TestCase):

    def test_init_game(self):
        from gravita.game import Game
        players = ('foo', 'bar')
        game = Game(players)
        self.assertEqual(game.players, players)
        self.assertEqual(len(game.map), 0)

    def test_init_map(self):
        from gravita.game import Game
        from gravita.sector import Sector
        players = ('foo', 'bar')
        game = Game(players)
        game.init_map(10, 20)
        self.assertEqual(len(game.map), 10)
        for col in game.map:
            self.assertEqual(len(col), 20)
            for row in col:
                self.assert_(isinstance(row, Sector), row)
                self.assertEqual(row.planet, None)
                self.assertEqual(row.ship, None)

    def test_map_indexing(self):
        from gravita.game import Game
        from gravita.sector import Sector
        players = ('foo', 'bar')
        game = Game(players)
        game.init_map(3, 5)
        for x, y in [(0,0), (-1,-1), (2,4), (1,2)]:
            sec = game.map[x][y]
            self.assert_(isinstance(sec, Sector))
        for x, y in [(3,5), (5,0), (100, 2)]:
            self.assertRaises(IndexError, lambda: game.map[x][y])


