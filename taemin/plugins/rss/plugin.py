#!/usr/bin/env python2
# -*- coding: utf8 -*-

from schema_rss import FeedEntry, Feed
from feed_thread import FeedThread
from taemin import schema, env

class TaeminRSS(object):
    def __init__(self, taemin):
        self.taemin = taemin
        self.conf = env.conf.get("RSS", {})
        if not self.conf:
            env.log.warning("Your RSS parser is not configure")

        self.feeds = []
        for rss, params in self.conf.iteritems():
            self.feeds.append(FeedThread(params.get("url", ""),
                                         self.on_newfeed,
                                         regex=params.get("regex", None),
                                         refresh=params.get("refresh", 60),
                                         name=rss))
        for feed in Feed.select().where(Feed.conf == False):
            self.feeds.append(FeedThread(feed.url, self.on_newfeed, name=feed.name))

        for feed in self.feeds:
            feed.start()

    def on_pubmsg(self, serv, msg):
        return
        if msg.key != "rss":
            return
        chan = msg.chan.name

        values = msg.value.split(" ", 1)
        if len(values) < 1:
            serv.privmsg(chan, "Usage: !rss add http//feed-url/")
            return

        key = values[0]
        value = values[1]

        if key == "add":
            feed = FeedThread(value, self.on_newfeed)
            feed.start()

    def get_feed(self, feed):
        if feed.regex:
            feed, test = Feed.get_or_create(name=feed.name, url=feed.rss, regex=feed.regex)
        else:
            feed, test = Feed.get_or_create(name=feed.name, url=feed.rss)
        return feed

    def get_entry(self, feed, title, link, chan):
        try:
            return FeedEntry.get(link=link, title=title, chan=chan)
        except FeedEntry.DoesNotExist:
            return None

    def on_newfeed(self, feed_thread, title, link):
        feed = self.get_feed(feed_thread)
        chans = None
        if feed.chan:
            chans = [feed.chan.name]

        if not chans:
            chans = self.conf.get(feed.name, {}).get("chans", [])

        if not chans:
            chans = self.taemin.chans

        for chan in chans:
            try:
                chan = schema.Chan.get(name=chan)
            except schema.Chan.DoesNotExist:
                env.log.warning("RSS plugin: %s is not a valid chan" % chan)
                continue

            entry = self.get_entry(feed, title, link, chan)
            if entry:
                continue
            self.taemin.connection.privmsg(chan.name, "[%s] %s: %s" % (feed.name, title, link))
            FeedEntry.create(chan=chan, feed=feed, title=title, link=link)

