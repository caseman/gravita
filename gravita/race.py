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
from gravita import ship


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
    """The Human race are a young species, but a few million years old.
    Their enormous ambition has brought them to the stars, and their
    adaptability and cunning have served them well in their extra-solar
    conquests. Although they have not sought to make the Naree and Rone
    their enemies, their expansionism puts them at odds with these
    powerful alien races.

    Humans hail from planet Earth, and thrive on Terran or Desert planets
    """

    name = 'Humans'
    home_planet_type = 'terran'

    planet_yields = planet.base_yields.copy()
    planet_yields['terran'] = planet.Yield(resources=5, research=3, bonus=6)
    planet_yields['desert'] = planet.Yield(resources=3, research=2, bonus=4)

    ship_specs = (ship.Columbus(), ship.Pegasus(), ship.MacArthur())


class Naree(Race):
    """The Naree are an ancient race that have long controlled vast regions of
    the galaxy. Their vast technology allows them to control the very fabric
    of space itself. Over the eons though, the Naree have grown arrogant,
    complacent, and unable to come to terms with change. Their vast empire
    is now threatened by the upstart Humans, and the insidious Rone.

    The origin of the Naree race is nearly as mysterious as that of the galaxy
    itself. Their biology is most suited to Ocean and Tundra planets.
    """

    name = 'Naree'
    home_planet_type = 'ocean'

    planet_yields = planet.base_yields.copy()
    planet_yields['ocean'] = planet.Yield(resources=5, research=3, bonus=6)
    planet_yields['tundra'] = planet.Yield(resources=3, research=2, bonus=4)

    ship_specs = (ship.Milfoil(), ship.Cress(), ship.Lotus())


class Rone(Race):
    """The Rone are an enigmatic, nomadic race that mysteriously appeared but
    a few decades ago. Their vast fleet forms a great conflagration bent on
    consuming everything in its path. Worlds to them are merely disposable
    vessels for the resources they contain. In their initial encounters with
    the Naree and Humans, they regarded them as little more than pests.
    However, they have proven to be stronger and more resilient then the Rone
    anticipated. This is considered to be only a temporary delay to their
    inevitable extinction, however.

    The Rone do not reside on planets, but can consume resources most
    efficiently from Swamp and Toxic worlds.
    """

    name = 'Naree'
    home_planet_type = 'swamp'

    planet_yields = planet.base_yields.copy()
    planet_yields['swamp'] = planet.Yield(resources=5, research=3, bonus=6)
    planet_yields['toxic'] = planet.Yield(resources=3, research=2, bonus=4)

    ship_specs = (ship.Scourge(), ship.Gotha(), ship.Draken())


races = {
    'human': Human(),
    'naree': Naree(),
    'rone': Rone(),
}
