#!/usr/bin/env python2
# -*- coding: utf8 -*-

class TaeminPlugin(object):
    helper = {}

    def __init__(self, taemin):
        self.taemin = taemin

    def start(self):
        pass

    def stop(self):
        pass

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

    def privmsg(self, chan, msg):
        """ Send a message to a chan or an user """

        if chan in self.taemin.chans:
            self.taemin.create_pub_message(self.taemin.name, chan, msg)
        else:
            self.taemin.create_priv_message(self.taemin.name, chan, msg)

        self.taemin.connection.privmsg(chan, msg)

    def expose_endpoints(self):
        """ Returns a list of all the endpoints the plugin wants to expose """
        return []
