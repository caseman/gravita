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



