##############################################################################
#
# Copyright (c) 2011 Casey Duncan
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT License
# A copy of the license should accompany this distribution.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
#############################################################################
import random
from gravita import markov
from gravita import planet


class Map(object):

    def __init__(self, width, height):
        """Initialize an empty game map"""
        self.width = width
        self.height = height
        self._sectors = {}
        for y in range(height):
            for x in range(width):
                self._sectors[x, y] = Sector()
        self._available_sectors = set(self._sectors)
        self._names = set()

    def __getitem__(self, location):
        return self._sectors[tuple(location)]

    def generate_planet_name(self):
        """Generate a unique planet name"""
        while 1:
            name = markov.generate('data/planet_names.txt')
            if len(name) > 3 and name not in self._names:
                for existing in self._names:
                    if existing.startswith(name) or name.startswith(existing):
                        break # Avoid names that prefix each other
                else:
                    self._names.add(name)
                    return name

    def add_planet(self, planet_type=None, location=None):
        """Add a planet to the map. The planet type and location can
        be specified, if not they will be randomly chosen.
        """
        if planet_type is not None:
            assert planet_type in planet.planet_types, \
                "Invalid planet type %s" % planet_type
        if location is None:
            assert self._available_sectors, "Cannot add planet, map is full"
            location = random.choice(list(self._available_sectors))
        x, y = location
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                self._available_sectors.discard((x + dx, y + dy))
        p = self[location].planet = planet.Planet(
            name=self.generate_planet_name(),
            type=planet_type or planet.next_planet_type(),
            location=location)
        return p

    def add_planets(self, count):
        """Populate the game map with random planets"""
        return [self.add_planet() for i in range(count)]

    def add_home_planets(self, players):
        """Create home planets for each specified player"""
        offset_x = self.width / 5
        offset_y = self.height / 5
        locations = [(offset_x, offset_y), 
            (self.width - offset_x - 1, self.height - offset_y - 1)]
        planets = []
        for player, location in zip(players, locations):
            home = self.add_planet(
                player.home_planet_type, 
                location=location)
            player.planets.add(home)
            planets.append(home)
        return planets


class Sector(object):

    def __init__(self):
        self.planet = None
        self.ship = None

    def __repr__(self):
        return '<Sector planet=%r ship=%r>' % (self.planet, self.ship)