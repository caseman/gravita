import unittest

class PlanetTestCase(unittest.TestCase):

    def test_init_planet(self):
        from gravita.planet import Planet
        p = Planet(name='foobar', type='ocean', location=(2,6))
        self.assertEqual(p.name, 'foobar')
        self.assertEqual(p.type, 'ocean')
        self.assertEqual(p.location, (2,6))
        
    def test_next_planet_type(self):
        from gravita import planet
        types = set()
        for i in range(100):
            type = planet.next_planet_type()
            self.assertTrue(type)
            self.assert_(type in planet.planet_types, type)
            types.add(type)
        self.assertEqual(types, set(planet.planet_types))

