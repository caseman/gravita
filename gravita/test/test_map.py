import unittest

class MapTestCase(unittest.TestCase):

    def test_init_map(self):
        from gravita.map import Map
        map = Map(10, 20)
        self.assertEqual(map.width, 10)
        self.assertEqual(map.height, 20)

    def test_sector_repr(self):
        from gravita.map import Map
        map = Map(3, 3)
        self.assertEqual(repr(map[1,1]), 
            '<Sector(1, 1) planet=None ship=None>')

    def test_map_indexing(self):
        from gravita.map import Map, Sector
        map = Map(3, 5)
        for x, y in [(0,0), (1,3), (2,4), (1,2)]:
            sec = map[x, y]
            self.assert_(isinstance(sec, Sector))
            self.assertEqual(sec.planet, None)
            self.assertEqual(sec.ship, None)
        for x, y in [(3,5), (5,0), (100, 2)]:
            self.assertRaises(KeyError, lambda: map[x, y])

    def test_generate_planet_name(self):
        from gravita.map import Map
        map = Map(7, 7)
        names = set()
        for i in range(100):
            name = map.generate_planet_name()
            self.assertFalse(name in names, name)
            names.add(name)

    def test_add_planet_random(self):
        from gravita.map import Map
        from gravita import planet
        for i in range(100):
            map = Map(7, 7)
            map.add_planet(location=(5, 5))
            p = map.add_planet()
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
            self.assertEqual(map[p.location].planet, p)

    def test_add_planet_fixed(self):
        from gravita.map import Map
        from gravita import planet
        map = Map(7, 7)
        p = map.add_planet('terran', (1,2))
        self.assert_(isinstance(p, planet.Planet))
        self.assertTrue(p.name)
        self.assertEqual(p.type, 'terran')
        self.assertEqual(p.location, (1,2))

    def test_add_planets(self):
        from gravita.map import Map
        from gravita import planet
        map = Map(12, 3)
        ps = map.add_planets(4)
        self.assertEqual(len(ps), 4)
        for p in ps:
            self.assertTrue(isinstance(p, planet.Planet))
            x, y = p.location
            self.assert_(0 <= x < 12, x)
            self.assert_(0 <= y < 3, y)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx or dy:
                        try:
                            self.assert_(map[x+dx, y+dy].planet is None,
                                [s[1].planet for s in sorted(map._sectors.items())
                                    if s[1].planet])
                        except KeyError:
                            pass

    def test_add_home_planets(self):
        from gravita.map import Map
        from gravita import planet
        players = (MockPlayer('terran'), MockPlayer('ocean'))
        map = Map(15, 10)
        ps = map.add_home_planets(players)
        self.assertEqual(len(ps), 2)
        self.assertEqual(len(players[0].planets), 1)
        self.assertEqual(len(players[1].planets), 1)
        p1_planet = iter(players[0].planets).next()
        p2_planet = iter(players[1].planets).next()
        self.assertEqual(p1_planet.type, 'terran')
        self.assertEqual(p1_planet.location, (3,2))
        self.assertEqual(p2_planet.type, 'ocean')
        self.assertEqual(p2_planet.location, (11,7))

    def test_sectors_in_circle_small(self):
        from gravita.map import Map
        map = Map(7, 7)
        sectors = map.sectors_in_circle((3, 3), 1)
        self.assertEqual(sectors,
            [map[2,2], map[3,2], map[4,2],
             map[2,3], map[3,3], map[4,3],
             map[2,4], map[3,4], map[4,4]], sectors)

    def test_sectors_in_circle_larger(self):
        from gravita.map import Map
        map = Map(15, 15)
        sectors = map.sectors_in_circle((5, 5), 3)
        self.assertEqual(sectors,
                               [map[4,2], map[5,2], map[6,2], 
                      map[3,3], map[4,3], map[5,3], map[6,3], map[7,3],
            map[2,4], map[3,4], map[4,4], map[5,4], map[6,4], map[7,4], map[8,4],
            map[2,5], map[3,5], map[4,5], map[5,5], map[6,5], map[7,5], map[8,5],
            map[2,6], map[3,6], map[4,6], map[5,6], map[6,6], map[7,6], map[8,6],
                      map[3,7], map[4,7], map[5,7], map[6,7], map[7,7],
                                map[4,8], map[5,8], map[6,8]])

    def test_sectors_in_circle_off_map(self):
        from gravita.map import Map
        map = Map(5, 5)
        sectors = map.sectors_in_circle((-1, -1), 2)
        self.assertEqual(sectors,
            [map[0,0], map[1,0],
             map[0,1]], sectors)



class MockPlayer(object):

    def __init__(self, hpt):
        self.home_planet_type = hpt
        self.planets = set()
