#!/usr/bin/env python3
# -*- coding: utf8 -*-

from threading import Thread
from flask import Flask
from taemin import logger

class HttpApiThread(Thread):
    """Thread which exposes plugins' HTTP API."""
    def __init__(self):
        """Creates the thread."""
        Thread.__init__(self)
        self.endpoints = []
        self._continue = False
        self.app = Flask(__name__)
        self.log = logger.Logger()

    def update_app(self):
        """Loads the endpoints in the Flask app. Needed befor exposition"""
        for endpoint in self.endpoints:
            full_route = endpoint.generate_route()
            self.log.debug("Route %s loaded" % full_route)
            endpoint.callback = self.app.route(full_route, methods=endpoint.methods)(endpoint.callback)

    def set_endpoints(self, endpoints):
        """Setter for the endpoints"""
        self.endpoints = endpoints

    def run(self):
        """Some gevent black magic to expose the app"""
        self._continue = True
        self.app.run()

    def stop(self):
        """Stops the HTTP API worker"""
        self._continue = False
