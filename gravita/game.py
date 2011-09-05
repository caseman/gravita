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
from gravita.map import Map

class Game(object):

    def __init__(self, players, map):
        assert len(players) == 2, 'Only two players are currently supported'
        self.players = players
        self.map = map
        self.turn = 0

    def begin_turn(self):
        """Begin a new turn in the game"""
        self.turn += 1
        for player in self.players:
            player.begin_turn()

