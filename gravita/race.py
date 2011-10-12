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
from gravita import planet


class Race(object):
    """Gravita race base class"""

    home_planet_type = None
    planet_yields = {}

    def total_yield(self, planets):
        yields = [self.planet_yields[ptype] for _, ptype, _ in planets]
        return (
            sum(y.resources for y in yields), 
            sum(y.research for y in yields)
        )


class Human(Race):
    """Humans hail from planet Earth, and thrive on Terran or Desert planets"""

    name = 'Humans'
    home_planet_type = 'terran'

    planet_yields = planet.base_yields.copy()
    planet_yields['terran'] = planet.Yield(resources=5, research=3, bonus=6)
    planet_yields['desert'] = planet.Yield(resources=3, research=2, bonus=4)


races = {
    'human': Human(),
    'naree': Human(),
    'rone': Human(),
}
