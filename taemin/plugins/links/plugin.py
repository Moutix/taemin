#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin, schema

class TaeminLinks(plugin.TaeminPlugin):
    helper = {
        "links": "Search for a specific link",
        "tag": "Tag a given link. Usage: !tag http://... tag1 tag2 ..."
    }

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        return {
            "links": self.on_links,
            "tag": self.on_tag
        }[msg.key](msg)


    def on_links(self, msg):
        chan = msg.chan.name

        links = [l for l in schema.Link.search(msg.value).limit(5)]

        if not links:
            self.privmsg(chan, "Aucun lien ne correspond")
            return

        for link in links:
            self.privmsg(chan, "[%s] %s (%s)" % (link.type, link.url, link.tags or link.title))

    def on_tag(self, msg):
        chan = msg.chan.name

        tags = msg.value.split(" ", 1)

        if len(tags) < 2:
            self.privmsg(chan, self.helper["tag"])
            return

        try:
            link = schema.Link.get(schema.Link.url == tags[0])
        except schema.Link.DoesNotExist:
            self.privmsg(chan, "%s is not a correct link" % tags[0])
            return

        link.tags = tags[1]
        link.save()
        self.privmsg(chan, "Tags ajoutés à ce lien: %s" % tags[1])
