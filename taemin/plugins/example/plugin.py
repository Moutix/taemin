#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin

class TaeminExample(plugin.TaeminPlugin):
    helper = {}

    def on_join(self, connection):
        pass

    def on_pubmsg(self, msg):
        pass

    def on_privmsg(self, msg):
        pass

    def on_quit(self, user):
        pass

    def on_part(self, connection):
        pass
