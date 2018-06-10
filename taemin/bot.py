""" Main bot file """

import datetime
import re
import ssl
import time
import threading

import irc.bot
import irc.client
import irc.connection

try:
    from importlib import reload
except ImportError:
    pass

from taemin import schema
from taemin import conf
from taemin import courriel
from taemin import logger
from taemin import sdnotify
# from taemin import profile

LINK_REGEX = re.compile(
    r'(https?://\S+\.\S+)',
    re.IGNORECASE
)

class Taemin(irc.bot.SingleServerIRCBot):
    def __init__(self, *args):
        self.sd_notify = sdnotify.get_notifier()
        self.conf = conf.get_config("taemin")
        self.conf.load(*args)

        general_conf = self.conf.get("general", {})
        self.chans = general_conf.get("chans")
        if not self.chans:
            self.chans = []
        self.name = general_conf.get("name", "Taemin")
        self.desc = general_conf.get("desc", "Le Splendide")
        self.server = general_conf.get("server", "")
        self.port = general_conf.get("port", 6667)
        self.tls = general_conf.get("tls", False)

        self.log = logger.Logger()
        self.mailation = courriel.Mailage(self)

        if self.tls == True:
            ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        else:
            ssl_factory = irc.connection.Factory()

        irc.bot.SingleServerIRCBot.__init__(self, [(self.server, self.port)], self.name, self.desc, connect_factory=ssl_factory)

        self.sd_notify.status("Load plugins...")

        self.plugins = self._get_plugins()
        self.user_init = {}

    def start(self):
        self.sd_notify.ready()
        super().start()

    def stop(self):
        """ Stop all running thread """

        for plugin in self.plugins:
            plugin.stop()

    def _nickserv_register(self):
        """Register the pseudo with nickserv"""
        password = self.conf.get("general", {}).get("nickserv", {}).get("pass")
        if not password:
            return

        self.connection.privmsg("NickServ", "IDENTIFY {}".format(password))

    def on_welcome(self, serv, ev):
        self._nickserv_register()

        query = schema.User.update(online=False)
        query.execute()
        for chan in self.chans:
            serv.join(chan)
            self.user_init[chan] = False

        for plugin in self.plugins:
            plugin.stop() # Be sure the plugin is stop before start
            plugin.start()

    def on_disconnect(self, serv, ev):
        """ When the connection with the socket is closed """

        self.stop()

    def on_join(self, serv, ev):
        source = self.get_nickname(ev.source.nick)
        if source == self.name:
            return

        chan = ev.target
        connection = self.connect_user(source, chan)

        self.safe_load_plugin("on_join", connection)

    #@profile.profile
    def on_pubmsg(self, serv, ev):
        source = self.get_nickname(ev.source.nick)
        target = ev.target
        message = ev.arguments[0]
        if not self.user_init[target]:
            self.init_users(target)

        msg = self.create_pub_message(source, target, message)

        if msg.key == "help":
            helper = {}
            for app in self.plugins:
                helper.update(app.helper)
            if msg.value in helper:
                serv.privmsg(target, helper[msg.value])
            else:
                serv.privmsg(target, "Usage: !help %s" % "|".join(helper.keys()))

        self.safe_load_plugin("on_pubmsg", msg)

    def on_privmsg(self, serv, ev):
        source = self.get_nickname(ev.source.nick)
        target = ev.target
        message = ev.arguments[0]

        msg = self.create_priv_message(source, target, message)

        self.safe_load_plugin("on_privmsg", msg)

    def on_part(self, serv, ev):
        name = self.get_nickname(ev.source.nick)
        chan = ev.target

        connection = self.disconnect_user_from_chan(name, chan)

        self.safe_load_plugin("on_part", connection)

    def on_quit(self, serv, ev):
        name = self.get_nickname(ev.source.nick)
        user = self.disconnect_user(name)

        self.safe_load_plugin("on_quit", user)

    def on_kick(self, serv, ev):
        nick = ev.arguments[0]
        channel = ev.target

        if nick == serv.get_nickname():
            time.sleep(1)
            serv.join(channel)

    def _get_plugins(self, force_reload=False):
        plugins = []
        for path, plugin_class in self.conf.get("plugins", {}).items():
            try:
                module = __import__("taemin.%s" % path, fromlist=[plugin_class])
                if force_reload:
                    reload(module)
                app = getattr(module, plugin_class)
                plugins.append(app(self))
                self.log.info("Load plugin: %s" % plugin_class)
            except Exception as e:
                self.log.exception("Plugin loading failed: %s\n%s", plugin_class, e)

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

    def get_user(self, name):
        try:
            user = schema.User.get(schema.User.name % name)
        except schema.User.DoesNotExist:
            return None
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

        mesg = schema.Message.create(
            user=user,
            message=message,
            key=key,
            value=value,
            chan=chan,
            link=schema.Link.new_from_url(self.find_link(message))
        )

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

    @staticmethod
    def find_link(message):
        m = LINK_REGEX.search(message)
        if not m:
            return None

        link = m.group(1)
        if link[-1] == ")" and "(" in message:
            link = link[:-1]

        return link

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
        self.sd_notify.reloading()
        self.log.info("Reload configuration")

        for plugin in self.plugins:
            plugin.stop()

        self.conf.reload()
        self.reload_chans()
        self.plugins = self._get_plugins(True)
        for plugin in self.plugins:
            plugin.start()

        self.log.info("Reload configuration done")
        self.sd_notify.ready()

    def reload_chans(self):
        new_chans = self.conf.get("general", {}).get("chans")
        if not new_chans:
            new_chans = []

        for chan in new_chans:
            if chan not in self.chans:
                self.connection.join(chan)
                self.user_init[chan] = False

        for chan in self.chans:
            if chan not in new_chans:
                self.connection.part([chan], "Bye :*")
        self.chans = new_chans

    def get_nickname(self, nick):
        if nick[0] in ("~", "&", "@", "%"):
            return nick[1:]
        return nick

    def safe_load_plugin(self, event, *opt):
        def run_safe(func, app):
            def safe_func(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                except Exception as err:
                    self.log.exception("Message %s %s %s",
                                       type(app).__name__, app.__module__, err)

            return safe_func

        for app in self.plugins:
            threading.Thread(target=run_safe(getattr(app, event), app), args=opt).start()

def main():
    name = "Ningirsu"
    chan = "#miku"

    taemin = Taemin()

if __name__ == "__main__":
    main()
