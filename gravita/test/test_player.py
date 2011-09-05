import unittest

class PlayerTestCase(unittest.TestCase):

    def test_init_player(self):
        from gravita.player import Player
        race = MockRace()
        player = Player('fooplayer', race)
        self.assertEqual(player.name, 'fooplayer')
        self.assert_(player.race is race)

    def test_begin_turn(self):
        from gravita.player import Player
        player = Player('bar', MockRace())
        player.ships.add('one')
        player.ships.add('two')
        self.assertFalse(player.to_move)
        self.assertFalse(player.actions_remaining)
        player.begin_turn()
        self.assertEqual(player.to_move, player.ships)
        self.assertEqual(player.actions_remaining, player.actions_per_turn)

    def test_begin_turn_updates_resources(self):
        from gravita.player import Player
        player = Player('bar', MockRace())
        self.assertEqual(player.resources, 0)
        self.assertEqual(player.research, 0)
        player.begin_turn()
        self.assertEqual(player.resources, 2)
        self.assertEqual(player.research, 1)
        player.begin_turn()
        self.assertEqual(player.resources, 4)
        self.assertEqual(player.research, 2)


class MockRace(object):

    def total_yields(self, planets):
        return 2, 1
