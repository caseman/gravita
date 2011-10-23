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

active_games = []


class Game(object):

    def __init__(self, map):
        self.players = []
        self.map = map
        self.turn = 0

    @property
    def in_progress(self):
        return self.turn > 0

    def add_player(self, player):
        assert len(self.players) < 2, 'Only two players are currently supported'
        assert not self.in_progress, 'Cannot add player, game already started'
        assert player not in self.players, 'Player already added to this game'
        self.players.append(player)

    def begin_turn(self):
        """Begin a new turn in the game"""
        #assert len(self.players) == 2, 'Too few players to start game'
        self.turn += 1
        for player in self.players:
            player.begin_turn()

    def as_dict(self, player):
        return {
            'turn': self.turn,
            'in_progress': self.in_progress,
            'map': self.map.as_dict(player.race),
            'players': [player.as_dict() for player in self.players]
            }

