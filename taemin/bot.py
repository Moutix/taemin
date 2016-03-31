#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot
import re
import database
import datetime
import courriel
import logger

from taemin import schema, conf

class Taemin(ircbot.SingleServerIRCBot):
    def __init__(self):
        self.conf = conf.TaeminConf().config

        general_conf = self.conf.get("general", {})
        self.chans = general_conf.get("chans", [])
        self.name = general_conf.get("name", "Taemin")
        self.desc = general_conf.get("desc", "Le Splendide")
        self.server = general_conf.get("server", "")
        self.port = general_conf.get("port", 6667)

        self.mailation = courriel.Mailage(self)
        self.log = logger.Logger()

        ircbot.SingleServerIRCBot.__init__(self, [(self.server, self.port)], self.name, self.desc)

        self.plugins = self._get_plugins()
        self.user_init = {}

    def on_welcome(self, serv, ev):
        query = schema.User.update(online=False)
        query.execute()

        for chan in self.chans:
            serv.join(chan)
            self.user_init[chan] = False

    def on_join(self, serv, ev):
        source = self.get_nickname(irclib.nm_to_n(ev.source()))
        if source == self.name:
            return

        chan = ev.target()
        connection = self.connect_user(source, chan)

        for plugin in self.plugins:
            plugin.on_join(connection)

    def on_pubmsg(self, serv, ev):
        source = self.get_nickname(irclib.nm_to_n(ev.source()))
        target = ev.target()
        message = ev.arguments()[0]
        if not self.user_init[target]:
            self.init_users(target)

        msg = self.create_pub_message(source, target, message)

        if msg.key == "help":
            helper = {}
            for plugin in self.plugins:
                helper.update(plugin.helper)
            if msg.value in helper:
                serv.privmsg(target, helper[msg.value])
            else:
                serv.privmsg(target, "Usage: !help %s" % "|".join(helper.keys()))

        for plugin in self.plugins:
            plugin.on_pubmsg(msg)

    def on_privmsg(self, serv, ev):
        source = self.get_nickname(irclib.nm_to_n(ev.source()))
        target = ev.target()
        message = ev.arguments()[0]

        msg = self.create_priv_message(source, target, message)

        for plugin in self.plugins:
            plugin.on_privmsg(msg)

    def on_part(self, serv, ev):
        name = self.get_nickname(irclib.nm_to_n(ev.source()))
        chan = ev.target()

        connection = self.disconnect_user_from_chan(name, chan)

        for plugin in self.plugins:
            plugin.on_part(connection)

    def on_quit(self, serv, ev):
        name = self.get_nickname(irclib.nm_to_n(ev.source()))
        user = self.disconnect_user(name)

        for plugin in self.plugins:
            plugin.on_quit(user)

    def _get_plugins(self, force_reload=False):
        plugins = []
        for path, plugin_class in self.conf.get("plugins", {}).iteritems():
            module = __import__("taemin.%s" % path, fromlist=[plugin_class])
            if force_reload:
                reload(module)
            plugin = getattr(module, plugin_class)
            plugins.append(plugin(self))
            self.log.info("Load plugin: %s" % plugin_class)
        return plugins


    def init_users(self, chan):
        for name in self.channels[chan].users():
            name = self.get_nickname(name)
            connection = self.find_connection(name, chan)
            user = connection.user
            user.online = True
            user.save()
        self.user_init[chan] = True

    def connect_user(self, name, chan):
        connection = self.find_connection(name, chan)
        connection.connected_at = datetime.datetime.now()
        connection.save()
        user = connection.user
        user.online = True
        user.save()
        return connection

    def disconnect_user_from_chan(self, name, chan):
        connection = self.find_connection(name, chan)
        connection.disconnected_at = datetime.datetime.now()
        connection.save()
        user = connection.user
        user.online = False
        user.save()
        return connection

    def disconnect_user(self, name):
        user = self.find_user(name)
        user.online = False
        user.save()
        query = schema.Connection.update(disconnected_at=datetime.datetime.now()).where(schema.Connection.user == user)
        query.execute()
        return user

    def list_users(self, chan, online=True):
        if online:
            return schema.User.select().where(schema.User.online == True).join(schema.Connection).where(schema.Connection.chan == chan)
        else:
            return schema.User.select().join(schema.Connection).where(schema.Connection.chan == chan)

    def list_user_name(self, chan):
        chan = self.find_chan(chan)
        return [user.name for user in self.list_users(chan)]

    def find_chan(self, name):
        chan, test = schema.Chan.get_or_create(name=name)
        return chan

    def find_user(self, name):
        try:
            user = schema.User.get(schema.User.name % name)
        except schema.User.DoesNotExist:
            user = schema.User.create(name=name)
        return user

    def find_connection(self, name, chan):
        chan = self.find_chan(chan)
        user = self.find_user(name)

        connection, test = schema.Connection.get_or_create(user=user, chan=chan)
        return connection

    def create_pub_message(self, source, target, message):
        key, value = self.parse_message(message)
        chan = self.find_chan(target)
        user = self.find_user(source)

        mesg = schema.Message.create(user=user, message=message, key=key, value=value, chan=chan)

        hl = []
        for user in self.list_users(chan, online=None):
            if re.compile("^.*" + user.name.lower() + ".*$").match(message.lower()):
                hl.append(user)
        mesg.highlights.add(hl)

        return mesg

    def create_priv_message(self, source, target, message):
        key, value = self.parse_message(message)
        user = self.find_user(source)

        mesg = schema.Message.create(user=user, message=message, key=key, value=value, target=target)
        return mesg

    def parse_message(self, message):
        m = re.search("^!(\S+)\s*(.*)$", message)
        if m:
            key = m.group(1).lower()
            value = m.group(2)
        else:
            key = None
            value = None

        return key, value

    def reload_conf(self):
        self.log.info("Reload configuration")
        self.conf = conf.TaeminConf().config
        self.plugins = self._get_plugins(True)
        self.log.info("Reload configuration done")

    def get_nickname(self, nick):
        if nick[0] in ("~", "&", "@", "%"):
            return nick[1:]
        return nick

def main():
    name = "Ningirsu"
    chan = "#miku"

    taemin = Taemin()

if __name__ == "__main__":
    main()

