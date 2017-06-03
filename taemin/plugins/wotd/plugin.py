""" Send a new ord every day """

import csv
import os
import threading
import datetime
import time
import random

from taemin import plugin

class WOTDCron(threading.Thread):
    """ Thread which send a word every day """

    def __init__(self, wotd_plugin):
        super().__init__()
        self.wotd_plugin = wotd_plugin

        self._continue = False

    def run(self):
        """ Cron which send wotd """

        self._continue = True

        while self._continue:
            if datetime.datetime.now().hour != self.wotd_plugin.hour:
                continue

            self.wotd_plugin.send_word()

            time.sleep(3600)

    def stop(self):
        """ Stop the thread """

        self._continue = False

class TaeminWOTD(plugin.TaeminPlugin):
    """ Taemin plugin to send new word every day """

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    DICO = os.path.join(__location__, "dico_rare.txt")

    helper = {}

    def __init__(self, taemin):
        super().__init__(taemin)

        self.words = list(self.get_words())
        self.conf = taemin.conf.get("wotd", {})
        self.chans = self.conf.get("chans", [])
        if not self.chans:
            self.chans = self.taemin.chans

        self.hour = int(self.conf.get("hour", 10))

        self.thread = WOTDCron(self)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()

    def pick_word(self):
        """ Pick a random word in the list """

        if not self.words:
            self.words = list(self.get_words())

        return self.words.pop(random.randint(0, len(self.words) - 1))

    def send_word(self):
        """ Send a new word to every chan """

        word = self.pick_word()

        for chan in self.chans:
            self.privmsg(chan, "WOTD: %s: %s" % (word["name"], word["description"]))

    @classmethod
    def get_words(cls):
        """ Get all the words in the dico"""
        with open(cls.DICO) as csvfile:
            for row in csv.DictReader(csvfile, fieldnames=["name", "description"]):
                yield row
