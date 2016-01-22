#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot
import re
from conf import TaeminConf
from database import DataBase

class Taemin(ircbot.SingleServerIRCBot):
    def __init__(self, conf):
        self.conf = conf.config
        general_conf = self.conf.get("general", {})
        db_conf = self.conf.get("database", {})

        self.db = DataBase(db_conf.get("type"),
                           name=db_conf.get("name"),
                           user=db_conf.get("user"),
                           password=db_conf.get("password"),
                           host=db_conf.get("host"))

        self.chans = general_conf.get("chans", [])
        self.name = general_conf.get("name", "Taemin")
        self.desc = general_conf.get("desc", "Le Splendide")
        self.server = general_conf.get("server", "")
        self.port = general_conf.get("port", 6667)
        ircbot.SingleServerIRCBot.__init__(self, [(self.server, self.port)], self.name, self.desc)

        self.plugins = self._get_plugins()

    def on_welcome(self, serv, ev):
        for chan in self.chans:
            serv.join(chan)

    def on_join(self, serv, ev):
        source = irclib.nm_to_n(ev.source())
        canal = ev.target()

        for plugin in self.plugins:
            if getattr(plugin, "on_join", None):
                plugin.on_join(serv, source=source, canal=canal)

    def on_pubmsg(self, serv, ev):
        canal = ev.target()
        source = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0]

        m = re.search("^!(\S+)\s*(.*)$", message)
        if m:
            key = m.group(1).lower()
            value = m.group(2)
        else:
            key = ""
            value = ""

        for plugin in self.plugins:
            if getattr(plugin, "on_pubmsg", None):
                plugin.on_pubmsg(serv, source=source, canal=canal, message=message, key=key, value=value)

    def on_privmsg(self, serv, ev):
        source = irclib.nm_to_n(ev.source())
        target = ev.target()
        message = ev.arguments()[0].lower()

        m = re.search("^!(\S+)\s*(.*)$", message)
        if m:
            key = m.group(1).lower()
            value = m.group(2)
        else:
            key = ""
            value = ""

        for plugin in self.plugins:
            if getattr(plugin, "on_privmsg", None):
                plugin.on_privmsg(serv, source=source, target=target, message=message, key=key, value=value)

    def _get_plugins(self):
        plugins = []
        for path, plugin_class in self.conf.get("plugins", {}).iteritems():
            module = __import__("taemin.%s" % path, fromlist=[plugin_class])
            plugin = getattr(module, plugin_class)
            plugins.append(plugin(self))
            print "Load plugin: %s" % plugin_class
        return plugins

def main():
    conf = TaeminConf()
    Taemin(conf).start()


if __name__ == "__main__":
    main()

