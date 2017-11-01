#!/usr/bin/env python3
# -*- coding: utf8 -*-

from threading import Thread
from flask import Flask

class HttpApiThread(Thread):
    def __init__(self, endpoints):
        Thread.__init__(self)
        self.endpoints = endpoints
        self._continue = false
        self.app = Flask(__name__)

    def update_app(self):
        """Generates the routes"""
        pass

    def run(self):
        self._continue = True
        """Some gevent black magic to expose the app""""

    def stop(self):
        self._continue = False

