#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot
import re
import datetime

from taemin import env, schema

class Taemin(ircbot.SingleServerIRCBot):
    def __init__(self):
        self.conf = env.conf
        general_conf = self.conf.get("general", {})
        self.chans = general_conf.get("chans", [])
        self.name = general_conf.get("name", "Taemin")
        self.desc = general_conf.get("desc", "Le Splendide")
        self.server = general_conf.get("server", "")
        self.port = general_conf.get("port", 6667)
        ircbot.SingleServerIRCBot.__init__(self, [(self.server, self.port)], self.name, self.desc)

        self.plugins = self._get_plugins()

    def on_welcome(self, serv, ev):
        query = schema.User.update(online=False)
        query.execute()
        query = schema.Connection.delete()
        query.execute()

        for chan in self.chans:
            serv.join(chan)

    def on_join(self, serv, ev):
        source = irclib.nm_to_n(ev.source())
        if source == self.name:
            return

        chan = ev.target()
        for name in self.channels[chan].users():
            connection = self.find_connection(name, chan)
            user = connection.user
            user.online = True
            user.save()

        connection = self.connect_user(source, chan)

        for plugin in self.plugins:
            if getattr(plugin, "on_join", None):
                plugin.on_join(serv, connection)

    def on_pubmsg(self, serv, ev):
        source = irclib.nm_to_n(ev.source())
        target = ev.target()
        message = ev.arguments()[0]

        msg = self.create_pub_message(source, target, message)

        for plugin in self.plugins:
            if getattr(plugin, "on_pubmsg", None):
                plugin.on_pubmsg(serv, msg)

    def on_privmsg(self, serv, ev):
        source = irclib.nm_to_n(ev.source())
        target = ev.target()
        message = ev.arguments()[0]

        msg = self.create_priv_message(source, target, message)

        for plugin in self.plugins:
            if getattr(plugin, "on_privmsg", None):
                plugin.on_privmsg(serv, msg)

    def on_part(self, serv, ev):
        name = irclib.nm_to_n(ev.source())
        chan = ev.target()

        connection = self.disconnect_user_from_chan(name, chan)

        for plugin in self.plugins:
            if getattr(plugin, "on_part", None):
                plugin.on_part(serv, connection=connection)

    def on_quit(self, serv, ev):
        name = irclib.nm_to_n(ev.source())

        user = self.disconnect_user(name)

        for plugin in self.plugins:
            if getattr(plugin, "on_quit", None):
                plugin.on_quit(serv, user)

    def _get_plugins(self):
        plugins = []
        for path, plugin_class in env.conf.get("plugins", {}).iteritems():
            module = __import__("taemin.%s" % path, fromlist=[plugin_class])
            plugin = getattr(module, plugin_class)
            plugins.append(plugin(self))
            print "Load plugin: %s" % plugin_class
        return plugins

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

    def list_users(self, chan):
        return schema.User.select().where(schema.User.online == True).join(schema.Connection).where(schema.Connection.chan == chan)

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
        for user in self.list_users(chan):
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

def main():
    name = "Ningirsu"
    chan = "#miku"

    taemin = Taemin()

    print taemin.find_connection(name, chan)
    print taemin.find_connection("Schnaffon", chan)
    print taemin.create_pub_message("Ningirsu", "coucou schnaffon :)", chan)
    print taemin.list_user_name("#miku")

if __name__ == "__main__":
    main()

