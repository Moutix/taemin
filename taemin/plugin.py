""" Base class for all taemin plugin """

import itertools

MAX_MSG_LENGTH = 400

class TaeminPlugin(object):
    helper = {}

    def __init__(self, taemin):
        self.taemin = taemin

    def start(self):
        pass

    def stop(self):
        pass

    def on_join(self, connection):
        pass

    def on_pubmsg(self, msg):
        pass

    def on_privmsg(self, msg):
        pass

    def on_quit(self, user):
        pass

    def on_part(self, connection):
        pass

    def privmsg(self, chan, msg):
        """ Send a message to a chan or an user """

        if not msg:
            return

        if not isinstance(msg, str):
            msg = msg.decode("utf-8")

        for m in ("".join(itertools.takewhile(lambda x: x, a)) for a in itertools.zip_longest(*([iter(msg)] * MAX_MSG_LENGTH))):
            print(m)
            if chan in self.taemin.chans:
                self.taemin.create_pub_message(self.taemin.name, chan, m)
            else:
                self.taemin.create_priv_message(self.taemin.name, chan, m)

            self.taemin.connection.privmsg(chan, m)
