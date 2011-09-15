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

class Ship(object):

    def __init__(self, map, location, specs):
        assert map[location].ship is None, "Ship already at %s" % location
        self.map = map
        self.location = location
        self.map[location].ship = self
        self.specs = specs

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

