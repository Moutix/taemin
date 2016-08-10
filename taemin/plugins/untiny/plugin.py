#!/usr/bin/env python2
# -*- coding: utf8 -*-

import requests

from taemin import plugin

class TaeminUntiny(plugin.TaeminPlugin):
    helper = {"untiny": "Get the real URL (untiny link for instance)"}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        new_url = self._url_to_untiny(msg.value)
        if not new_url:
            self.privmsg(chan, "Not a valid url")
            return

        self.privmsg(chan, "Real URL: %s" % new_url)

    def _url_to_untiny(self, url):
        try:
            return requests.get(url).url
        except requests.exceptions.RequestException as err:
            return None

