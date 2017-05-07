#!/usr/bin/env python2
# -*- coding: utf8 -*-

import requests

from taemin import plugin

class TaeminTiny(plugin.TaeminPlugin):
    helper = {"tiny": "Transform an URL to a tiny URL"}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        new_url = self._url_to_tiny(msg.value)
        if not new_url:
            self.privmsg(chan, "Not a valid url")
            return

        self.privmsg(chan, "Tiny URL: %s" % new_url)

    def _url_to_tiny(self, url):
        try:
            tinyurl = requests.get("http://tinyurl.com/api-create.php", params={"url": url}).text
        except requests.exceptions.RequestException:
            return None
        return tinyurl
