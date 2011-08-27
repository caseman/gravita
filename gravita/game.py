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
from gravita.sector import Sector

class Game(object):

    def __init__(self, players):
        self.players = players
        self.map = []
        self.turn = 0

    def init_map(self, width, height):
        """Initialize an empty game map"""
        self.map = tuple(tuple(Sector() for y in range(height)) 
            for x in range(width))

