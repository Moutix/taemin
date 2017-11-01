#!/usr/bin/env python3
# -*- coding: utf8 -*-

class HttpApiEndpoint():
    """Object used by plugins to declare their endpoints to the HTTP API thread."""
    def __init__(self, plugin, route, callback, methods=['GET']):
        """Creates the Endpoint"""
        self.plugin = plugin
        self.route = route
        self.callback = callback
        self.methods = methods

    def generate_route(self):
        """Computes the full route by adding the plugin name and the relative route.
        For example the plugin 'plugin' wants to expose the route 'route',
        the full route will be '/plugin/route' """
        return '/' + self.plugin + '/' + self.route
