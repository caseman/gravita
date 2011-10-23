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

class Player(object):

    actions_per_turn = 1

    def __init__(self, number, name, race, color):
        self.number = number
        self.name = name
        self.race = race
        self.color = color
        self.planets = set()
        self.ships = set()
        self.to_move = set()
        self.actions_remaining = 0
        self.resources = 0
        self.research = 0

    def begin_turn(self):
        """Begin a new turn for the player, update the resources,
        research, move, and action counts
        """
        self.actions_remaining = self.actions_per_turn
        resources, research = self.race.total_yield(self.planets)
        self.resources += resources
        self.research += research
        for ship in self.ships:
            ship.begin_turn()

    def as_dict(self):
        return {
            'number': self.number,
            'name': self.name,
            'race': self.race.name,
            'color': self.color,
            }

