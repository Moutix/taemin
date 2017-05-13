#!/usr/bin/env python3
# -*- coding: utf8 -*-

from threading import Thread
import time
import re
import feedparser

class FeedThread(Thread):
    def __init__(self, rss, callback, regex=None, refresh=60, name=None):
        Thread.__init__(self)
        self.name = name
        self.rss = rss
        self.callback = callback
        self.regex = regex
        self.refresh = refresh
        self._continue = False

    def get_feeds(self):
        feeds = feedparser.parse(self.rss)
        if feeds.get("bozo_exception"):
            pass
        else:
            self.name = feeds.feed.get("title", self.name)

        return feeds

    def get_entries(self):
        entries = []
        feeds = self.get_feeds()
        if not self.regex:
            return feeds.entries

        for entry in feeds.entries:
            if re.search(self.regex, entry["title"]) != None:
                entries.append(entry)
        return entries

    def run(self):
        self._continue = True

        time.sleep(2)
        while self._continue:
            entries = self.get_entries()
            if len(entries) > 5:
                entries = entries[:5]
            for entry in entries:
                self.callback(self, entry.get("title", ""), entry.get("link", ""))
            time.sleep(self.refresh)

    def stop(self):
        self._continue = False

def main():
    def callback(feed, title, link):
        print("%s: %s" % (title, link))

    rss = "http://sametmax.com/feed/"
    feed = FeedThread(rss, callback, refresh=2)
    feed.start()

if __name__ == "__main__":
    main()
