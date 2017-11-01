#!/usr/bin/env python3
# -*- coding: utf8 -*-

class HttpApiEndpoint():
    def __init__(self, plugin, route, callback, methods=['GET']):
        self.plugin = plugin
        self.route = route
        self.callback = callback
        self.methods = methods

    def generate_route(self):
        return('/' + self.plugin + '/' + self.route)
