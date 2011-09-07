import unittest

class RaceTestCase(unittest.TestCase):

    def test_init_human(self):
        from gravita import planet
        from gravita.race import Human
        h = Human()
        self.assertTrue(h.name)
        self.assertTrue(h.home_planet_type in planet.planet_types,
            h.home_planet_type)

    def test_planet_yields(self):
        from gravita import planet
        from gravita.race import Human
        h = Human()
        for planet_type in planet.planet_types:
            y = h.planet_yields[planet_type]
            self.assertTrue(y.resources >= 0)
            self.assertTrue(y.research >= 0)
            self.assertTrue(y.bonus >= 0)

    def test_total_yields(self):
        from gravita.race import Human
        h = Human()
        self.assertEqual(h.total_yield([]), (0, 0))
        planets = [
            (None, 'terran', None),
            (None, 'desert', None),
            (None, 'ocean', None),
        ]
        r1, r2 = h.total_yield(planets)
        self.assertTrue(r1 > 0)
        self.assertTrue(r2 > 0)
