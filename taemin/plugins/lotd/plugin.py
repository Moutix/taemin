""" Send a new ord every day """

import threading
import datetime
import time

from taemin import plugin
from taemin import schema

class LOTDCron(threading.Thread):
    """ Thread which send a word every day """

    def __init__(self, lotd_plugin):
        super().__init__()
        self.lotd_plugin = lotd_plugin

        self._continue = False

    def run(self):
        """ Cron which send wotd """

        self._continue = True

        while self._continue:
            if datetime.datetime.now().hour != self.lotd_plugin.hour:
                time.sleep(60)
                continue

            self.lotd_plugin.send_links()

            time.sleep(3600)

    def stop(self):
        """ Stop the thread """

        self._continue = False

class TaeminLOTD(plugin.TaeminPlugin):
    """ Taemin plugin to send new word every day """

    helper = {}

    def __init__(self, taemin):
        super().__init__(taemin)

        self.conf = taemin.conf.get("lotd", {})
        self.chans = self.conf.get("chans", [])
        if not self.chans:
            self.chans = self.taemin.chans

        self.hour = int(self.conf.get("hour", 21))

        self.thread = LOTDCron(self)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()


    def send_links(self):
        """ Send list of all links pass in the chan """

        for chan in self.chans:

            links = list(
                schema.Link
                .select()
                .where(
                    (schema.Link.created_at > datetime.datetime.utcnow() - datetime.timedelta(days=1))
                )
            )
            if not links:
                self.taemin.log("LOTD: No links to display for chan %s", chan)
                continue

            self.privmsg(chan, "Link of the day: %s links today:" % len(links))
            for link in links:
                self.privmsg(chan, "%s - %s" % (link.url, link.title))
