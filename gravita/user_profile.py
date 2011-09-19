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
import random
import sys
from gravita import markov

_profiles = {}

def clear_all():
    """Clear all persisted User profiles"""
    global _profiles
    _profiles.clear()


class UserProfile(object):

    def __init__(self):
        global _profiles
        while 1:
            self.profile_id = self.generate_id()
            if self.profile_id not in _profiles:
                _profiles[self.profile_id] = self
                break
        self.name = self.generate_name()
        self.game = None

    @classmethod
    def load(self, profile_id):
        """Load a UserProfile instance from persistence"""
        return _profiles[profile_id]

    def generate_id(self):
        """Generate a unique id for this profile"""
        return hex(id(self) ^ random.randint(sys.maxint >> 16, sys.maxint))[2:]

    def generate_name(self):
        """Generate a profile name"""
        while 1:
            name = markov.generate('data/profile_names.txt')
            if len(name) >= 5:
                return name


