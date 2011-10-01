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
import os
from pyramid.response import Response
from pyramid.view import view_config


class GravitaView(object):
    def __init__(self, request):
        self.request = request

    @view_config()
    def main(self):
        here = os.path.dirname(__file__)
        content = open(os.path.join(here, 'www', 'index.html'))
        return Response(content_type='text/html', app_iter=content)

