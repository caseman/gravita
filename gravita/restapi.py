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
from pyramid.view import view_config
from gravita.user_profile import UserProfile
from gravita.player import Player
from gravita.race import races
from gravita.game import Game, active_games
from gravita.map import Map


class RestApi(object):
    """Gravita rest api exposed to web clients"""

    def __init__(self, request):
        self.request = request
        self.response = request.response

    def get_user_profile(self):
        """Return the UserProfile instance for the given request, or
        create one if none is found.
        """
        try:
            return UserProfile.load(self.request.cookies['profile']), False
        except KeyError:
            profile = UserProfile()
            self.response.set_cookie('profile', profile.profile_id)
            return profile, True

    @view_config(name='profile_info', renderer='json')
    def profile_info(self):
        profile, is_new = self.get_user_profile()
        return {
            'profile_id': profile.profile_id, 
            'name': profile.name,
            'in_game': profile.game is not None,
            'is_new': is_new,
            }

    @view_config(name='create_game', renderer='json', request_method='POST')
    def create_game(self):
        params = self.request.POST
        profile, is_new = self.get_user_profile()
        map_width = map_height = int(params['map_size'])
        game_map = Map(map_width, map_height)
        game_map.add_planets(int(float(params['density']) * map_width * map_height))
        profile.game = Game(game_map)
        race = races[params['race']]
        player = Player(1, profile.name, race, params['color'])
        profile.game.add_player(player)
        active_games.append(profile.game)
        from random import randint, choice
        from gravita.ship import Ship
        for i in range(5):
            x = randint(0, map_width - 1)
            y = randint(0, map_height - 1)
            game_map[x, y].ship = ship = Ship(player, game_map, (x,y), choice(race.ship_specs))

        return profile.game.as_dict()

    @view_config(name='map', renderer='json')
    def map(self):
        profile, is_new = self.get_user_profile()
        return profile.game.map.as_dict()

    @view_config(name='players', renderer='json')
    def players(self):
        profile, is_new = self.get_user_profile()
        players = [player.as_dict() for player in profile.game.players]

    @view_config(name='ship_moves', renderer='json')
    def ship_moves(self):
        profile, is_new = self.get_user_profile()
        ship = profile.game.map.ships[self.request.GET['ship_id']]
        sectors = profile.game.map.sectors_in_circle(ship.location, ship.specs.range)
        return [sector.as_dict() for sector in sectors if sector.ship is None]

    @view_config(name='move_ship', renderer='json', request_method='POST')
    def move_ship(self):
        params = self.request.POST
        profile, is_new = self.get_user_profile()
        ship = profile.game.map.ships[params['ship_id']]
        location = (int(params['x']), int(params['y']))
        ship.move_to(location)
        return ship.as_dict()




