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
                self._sectors[x, y] = Sector(x, y)
        self._available_sectors = set(self._sectors)
        self._names = set()
        self.ships = {}

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
            location=location,
            size=random.random() * 0.7 + 0.3)
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

    def sectors_in_circle(self, center_location, radius):
        """Return a list of sectors on the map within radius sectors
        of the specified center location. Note the center location does
        not need to be on the map.

        The list of sectors is returned in lexicographical order.
        """
        cx, cy = center_location
        sectors = []
        limit = radius * radius + 1
        for y in range(cy - radius, cy + radius + 1):
            dy = y - cy
            for x in range(cx - radius, cx + radius + 1):
                dx = x - cx
                if dx*dx + dy*dy <= limit:
                    try:
                        sectors.append(self[x, y])
                    except KeyError:
                        pass
        return sectors

    def as_dict(self, race=None):
        d = {}
        d['width'] = self.width
        d['height'] = self.height
        d['sectors'] = sectors = []
        d['ships'] = ships = {}
        for y in range(self.height):
            row = []
            for x in range(self.width):
                sec = self._sectors[x, y]
                row.append(sec.as_dict(race))
                if sec.ship is not None:
                    ships[sec.ship.id] = sec.ship.as_dict()
            sectors.append(row)
        return d


class Sector(object):

    def __init__(self, x, y):
        self.planet = None
        self.ship = None
        self.location = (x, y)

    def as_dict(self, race=None):
        if race is not None:
            yields = race.planet_yields
        else:
            yields = planet.base_yields
        d = {
            'x': self.location[0],
            'y': self.location[1],
        }
        if self.planet is not None:
            pname, ptype, _, size = self.planet
            d['planet'] = {
                'name': pname, 
                'type': ptype, 
                'size': size,
                'resources':yields[ptype].resources,
                }
        return d

    def __repr__(self):
        return '<Sector%r planet=%r ship=%r>' % (self.location, self.planet, self.ship)
