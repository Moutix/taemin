#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
import requests
from bs4 import BeautifulSoup
from taemin import plugin

class TaeminNiceBot(plugin.TaeminPlugin):

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.mapping = [
            (r"""((?:http[s]?://)?(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-]+)(&(amp;)?[\w\?=]*)?)""", self._get_youtube),
            (r"""(https?://\S+)""", self._get_title),
        ]

    def on_pubmsg(self, msg):
        chan = msg.chan.name

        for match in self.check_generator(msg.message):
            self.privmsg(chan, match)

    def check_generator(self, text):
        for regex, func in self.mapping:
            match = re.search(regex, text)
            if not match:
                continue

            res = func(match, text)
            if res:
                yield res
                break

    def _get_title(self, match, text):
        try:
            html = requests.get(match.group(1))
        except requests.RequestException:
            return None

        try:
            html = html.text
        except TypeError:
            return None

        html = BeautifulSoup(html, 'html.parser')

        title = html.find("title")
        if not title:
            return None

        return title.string.strip().encode("utf-8")

    def _get_youtube(self, match, text):
        try:
            html = requests.get(match.group(1)).text
        except requests.RequestException:
            return None

        html = BeautifulSoup(html, 'html.parser')

        user = self.get_youtube_user(html) or ""
        title = self.get_youtube_title(html)
        if not title:
            return None

        return "%s: %s" % (user, title)

    def get_youtube_title(self, html):
        title = html.find(id="eow-title")
        if not title:
            return None

        return title.string.strip().encode("utf-8")

    def get_youtube_user(self, html):
        user = html.select("div.yt-user-info a.yt-uix-sessionlink")
        if not user:
            return None

        return user[0].string.strip().encode("utf-8")

def main():
    nice = TaeminNiceBot(None)
    for match in nice.check_generator("test ça : https://www.youtube.com/watch?v=0rtV5esQT6I"):
        print(match)

if __name__ == "__main__":
    main()

