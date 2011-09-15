import unittest
from collections import namedtuple

MockSpecs = namedtuple("MockSpecs", "range")

class ShipTestCase(unittest.TestCase):

    def test_init_ship(self):
        from gravita.ship import Ship
        map = {(1,1): MockSector(1,1)}
        specs = MockSpecs(range=1)
        ship = Ship(map, (1,1), specs)
        self.assertEqual(ship.location, (1, 1))
        self.assertEqual(ship.specs, specs)
        self.assert_(map[1,1].ship is ship)

    def test_available_moves_clear(self):
        from gravita.ship import Ship
        map = MockMap()
        specs = MockSpecs(range=2)
        ship = Ship(map, (1,1), specs)
        available = set(map.values())
        available.remove(map[1,1])
        self.assertEqual(set(ship.available_moves()), available)

    def test_available_moves_excludes_sectors_with_ships(self):
        from gravita.ship import Ship
        map = MockMap()
        specs = MockSpecs(range=2)
        map[0,0].ship = Ship(map, (0,0), specs)
        map[0,1].ship = Ship(map, (0,1), specs)
        map[1,2].ship = Ship(map, (1,2), specs)
        ship = Ship(map, (1,1), specs)
        self.assertEqual(set(ship.available_moves()), 
            set([map[1,0], map[2,0], map[2,1], map[0,2], map[2,2]]))

    def test_move_to(self):
        from gravita.ship import Ship
        map = MockMap()
        specs = MockSpecs(range=2)
        ship = Ship(map, (0,1), specs)
        self.assertEqual(map[2,0].ship, None)
        ship.move_to((2,0))
        self.assertEqual(map[2,0].ship, ship)
        for sector in map.values():
            if sector.location != (2, 0):
                self.assertEqual(sector.ship, None)


class MockSector(object):

    def __init__(self, x, y):
        self.location = x, y
        self.ship = None


class MockMap(dict):

    def __init__(self):
        for y in range(3):
            for x in range(3):
                self[x, y] = MockSector(x, y)

    def sectors_in_circle(self, location, radius):
        return self.values()
