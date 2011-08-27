import unittest

class PlanetTestCase(unittest.TestCase):

    def test_next_planet_type(self):
        from gravita import planet
        types = set()
        for i in range(100):
            type = planet.next_planet_type()
            self.assertTrue(type)
            self.assert_(type in planet.planet_types, type)
            types.add(type)
        self.assertEqual(types, set(planet.planet_types))

    def make_map(self):
        return [[DummySector() for y in range(7)] for x in range(7)]

    def test_check_location_empty_map(self):
        from gravita import planet
        map = self.make_map()
        for y in range(7):
            for x in range(7):
                self.assertTrue(planet.check_location(map, x, y), (x, y))

    def test_check_location(self):
        from gravita import planet
        map = self.make_map()
        map[0][0].planet = 'foo'
        map[5][5].planet = 'bar'
        for x, y in [(0,0), (0,1), (1,1), (1,0), 
            (4,4), (5,4), (5,5), (6,4), (6,6)]:
            self.assertFalse(planet.check_location(map, x, y), (x, y))
        for x, y in [(0,2), (0,3), (1,4), (2,0), (2,2), 
            (3,3), (2,3), (2,5), (0,7), (7,7)]:
            self.assertTrue(planet.check_location(map, x, y), (x, y))

    def test_create_planet(self):
        from gravita import planet
        map = self.make_map()
        map[5][5].planet = 'bar'
        for i in range(100):
            p = planet.create_planet(map)
            self.assert_(isinstance(p, planet.Planet))
            x, y = p.location
            self.assert_(0 <= x < 7, x)
            self.assert_(0 <= y < 7, y)
            self.assert_((x,y) not in [
                (4,4), (5,4), (6,4), 
                (4,5), (5,5), (6,5),
                (4,6), (5,6), (7,6),], (x,y))
            self.assertTrue(p.name)
            self.assert_(p.type in planet.planet_types, p.type)


class DummySector(object):

    def __init__(self):
        self.planet = None
        self.ship = None

