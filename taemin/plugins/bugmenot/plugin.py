#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from taemin.plugins.bugmenot.bugmenot import BugMeNot

class TaeminBugMeNot(plugin.TaeminPlugin):
    helper = {"login": "Return a login for the given url"}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        login = BugMeNot.login(msg.value)
        if not login:
            self.privmsg(chan, "No login found for this url")
            return

        self.privmsg(chan, "Username: {username}, Password: {password}".format(
            username=login["username"],
            password=login["password"]
        ))
