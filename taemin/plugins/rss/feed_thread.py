#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import env
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

    def get_feeds(self):
        feeds = feedparser.parse(self.rss)
        if feeds.get("bozo_exception"):
            env.log.warning(feeds["bozo_exception"])
        else:
            self.name = feeds.feed.get("title", self.name)
            env.log.info("Successfuly add feed %s" % self.name)

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
        time.sleep(2)
        while True:
            entries = self.get_entries()
            if len(entries) > 5:
                entries = entries[-5:]
            for entry in entries:
                self.callback(self, entry.get("title", "").encode("utf-8"), entry.get("link", "").encode("utf-8"))
            time.sleep(self.refresh)

def main():
    def callback(feed, title, link):
        print "%s: %s" % (title, link)

    rss = "http://feeds.feedblitz.com/SenorGif"
    feed = FeedThread(rss, callback)
    feed.start()

if __name__ == "__main__":
    main()
