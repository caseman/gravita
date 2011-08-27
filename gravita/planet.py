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
from gravita import markov
from collections import namedtuple
import random
import itertools

Planet = namedtuple("Planet", "name type location")

planet_info = (
    ('barren', 5),
    ('desert', 4),
    ('giant', 5),
    ('inferno', 2),
    ('ocean', 3),
    ('radiated', 2),
    ('swamp', 3),
    ('terran', 3),
    ('toxic', 2),
    ('tundra', 4),
)
planet_types = [info[0] for info in planet_info]

planet_likelyhood = []
for ptype, likelyhood in planet_info:
    planet_likelyhood.extend([ptype] * likelyhood)
random.shuffle(planet_likelyhood)
next_planet_type = itertools.cycle(planet_likelyhood).next

def check_location(game_map, x, y):
    """Return True if the x, y location on the game map is appropriate
    for a planet.
    """
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            try:
                if game_map[x+dx][y+dy].planet is not None:
                    return False
            except IndexError:
                pass
    return True

names = set()
def generate_name():
    """Generate a unique planet name"""
    while 1:
        name = markov.generate('data/planet_names.txt')
        if len(name) > 3 and name not in names:
            for existing in names:
                if existing.startswith(name) or name.startswith(existing):
                    break # Avoid names that prefix each other
            else:
                names.add(name)
                return name


def create_planet(game_map, planet_type=None, location=None):
    max_x = len(game_map) - 1
    max_y = len(game_map[0]) - 1
    while location is None:
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        if check_location(game_map, x, y):
            location = (x, y)
    return Planet(name=generate_name(),
        type=planet_type or next_planet_type(),
        location=location)


