#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from flask import request
from ...http_api_endpoint import HttpApiEndpoint

class TaeminHttPing(plugin.TaeminPlugin):
    helper = {}

    def ping_chan(self, chan):
        """Method called by the HTTP API that send a ping to a chan"""
        chan = '#'+chan
        subject = request.args.get('subject')
        if subject is None:
            message = "ping from http without any subject"
        else:
            message = "ping from http : %s" % subject
        self.privmsg(chan, message)
        return "Chan pinged"

    def ping_user(self, user):
        """Method called by the HTTP API that send a ping to a user"""
        subject = request.args.get('subject')
        if subject is None:
            message = "ping from http without any subject"
        else:
            message = "ping from http : %s" % subject
        self.privmsg(user, message)
        return "User pinged"

    def expose_endpoints(self):
        """Exposes endpoints to the API"""
        endpoints = []
        endpoints.append(HttpApiEndpoint('HttPing', 'chan/<string:chan>', self.ping_chan, methods=['GET']))
        endpoints.append(HttpApiEndpoint('HttPing', 'user/<string:user>', self.ping_user, methods=['GET']))
        return endpoints
