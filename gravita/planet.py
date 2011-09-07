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

Yield = namedtuple("Yield", "resources research bonus")

base_yields = {
    'barren': Yield(resources=1, research=0, bonus=1),
    'desert': Yield(resources=1, research=1, bonus=2),
    'giant': Yield(resources=2, research=1, bonus=2),
    'inferno': Yield(resources=2, research=1, bonus=3),
    'ocean': Yield(resources=3, research=2, bonus=6),
    'radiated': Yield(resources=1, research=2, bonus=3),
    'swamp': Yield(resources=3, research=2, bonus=6),
    'terran': Yield(resources=3, research=2, bonus=6),
    'toxic': Yield(resources=0, research=1, bonus=1),
    'tundra': Yield(resources=1, research=2, bonus=4),
}


