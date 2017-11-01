#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from ...http_api_endpoint import HttpApiEndpoint

class TaeminHttPing(plugin.TaeminPlugin):
    helper = {}

    def ping_chan(self,chan):
        chan = '#'+chan
        self.privmsg(chan, 'ping from http')
        return "Chan pinged"

    def expose_endpoints(self):
        endpoints = []
        endpoints.append(HttpApiEndpoint('HttPing', 'chan/<string:chan>', self.ping_chan, methods=['GET']))
        return endpoints
