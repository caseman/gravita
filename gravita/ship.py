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
import json
from collections import namedtuple

class Ship(object):

    def __init__(self, owner, map, location, specs):
        assert map[location].ship is None, "Ship already at %s" % location
        self.owner = owner
        self.map = map
        self.location = location
        self.specs = specs
        self.id = hex(id(self))[2:]
        self.level = id(owner) % 5
        self.variant = id(self) % 4
        map.ships[self.id] = self
        self.map[location].ship = self
        self.hp = self.specs.max_hp
        self.ap = self.specs.max_ap

    def available_moves(self):
        return [sector for sector in 
            self.map.sectors_in_circle(self.location, self.specs.range)
            if sector.ship is None]

    def move_to(self, location):
        assert self.map[location].ship is None, "Ship already at %s" % location
        old_location = self.location
        self.map[old_location].ship = None
        self.map[location].ship = self
        self.location = location
        return old_location, self.location

    def begin_turn(self):
        self.ap = self.specs.max_ap

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def as_dict(self):
        return {
            'owner': self.owner.as_dict(),
            'specs': self.specs.as_dict(),
            'cls': self.specs.cls, 
            'name': self.specs.name,
            'descr': self.specs.descr,
            'id':self.id,
            'race': self.specs.race,
            'range': self.specs.range,
            'level': self.level, 
            'variant': self.variant,
            'x': self.location[0],
            'y': self.location[1],
            'hp': self.hp,
            'ap': self.ap,
            }

def dictify(obj, base):
    d = dict(base.__dict__)
    d.update(obj.__class__.__dict__)
    d.update(obj.__dict__)
    for key, val in list(d.items()):
        if key.startswith('_'):
            del d[key]
        else:
            try:
                json.dumps(val)
            except TypeError:
                del d[key]
    return d

class Spec(object):
    """Ship specification"""

    def __init__(self):
        self.name = self.__class__.__name__

    def as_dict(self):
        d = dictify(self, Spec)
        d['weapons'] = [weapon.as_dict() for weapon in self.weapons]
        return d

class Weapon(object):
    """Weapon specification"""
    is_offense = True
    is_defense = True
    is_ranged = False

    def as_dict(self):
        return dictify(self, Weapon)

# Rone ship specs

class Scourge(Spec):
    cls = 0
    descr="Fighter"
    race = "rone"
    cost = 10
    range = 4
    move_ap = 2
    max_ap = 10
    max_hp = 24

    class _disruptor(Weapon):
        name = "Phase Disruptor"
        dmg_type = "electromag"
        dmg_level = 3
        max_use = 3
        use_ap = 2

    weapons = [_disruptor()]

class Gotha(Spec):
    cls = 2
    descr="Bomber"
    race = "rone"
    cost = 22
    range = 4
    move_ap = 3
    max_ap = 15
    max_hp = 38

    class _bomb(Weapon):
        name = "Incendiary Bomb"
        dmg_type = "thermal"
        dmg_level = 7
        max_use = 2
        use_ap = 4
        is_defense = False

    class _turret(Weapon):
        name = "Flak Turret"
        dmg_type = "impact"
        dmg_level = 3
        max_use = 4
        use_ap = 2
        is_ranged = True

    weapons = [_bomb(), _turret()]

class Draken(Spec):
    cls = 4
    descr="Dreadnought"
    race = "rone"
    cost = 39
    range = 4
    move_ap = 5
    max_ap = 25
    max_hp = 70

    class _cannon(Weapon):
        name = "Heavy Plasma Cannon"
        dmg_type = "thermal"
        dmg_level = 12
        max_use = 2
        use_ap = 5
        is_ranged = True

    class _turret(Weapon):
        name = "Magneto Pulse"
        dmg_type = "electromag"
        dmg_level = 25
        max_use = 1
        use_ap = 15

    weapons = [_cannon(), _turret()]


Spec = namedtuple("Spec", "cls name descr race cost range") # max_hp max_ap move_ap weapons")

Weapon = namedtuple("WeaponSpec", "name dmg_type dmg_level use_ap max_use is_offense is_defense")

