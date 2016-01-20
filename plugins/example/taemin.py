#!/usr/bin/env python2
# -*- coding: utf8 -*-

class TaeminExample(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_join(self, serv, source, **kwargs):
        pass

    def on_pubmsg(self, serv, canal, message, key, value, **kwargs):
        pass

    def on_privmsg(self, serv, target, key, value, **kwargs):
        pass



