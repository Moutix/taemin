""" Parse the kimsuffi page to find available server """

import time
import json
from threading import Thread

import requests

from taemin import plugin

URL = "https://www.kimsufi.com/fr/serveurs.xml"

class KimsuffiSearch(Thread):
    """ Thread which parse the kimsuffi page  """

    URL_AVAILABILITY = "https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2?callback=Request.JSONP.request_map.request_0"

    def __init__(self, callback, refresh=60, model="160sk1"):
        Thread.__init__(self)
        self.callback = callback
        self.refresh = refresh
        self.model = model

        self._state_available = False
        self._continue = False

    def run(self):
        self._continue = True
        while self._continue:
            available = self.get_server_availability(model=self.model)
            if self._state_available != available:
                self.callback(available)
                self._state_available = available

            time.sleep(self.refresh)

    def get_server_availability(self, model):
        """ Return the availability of a server if available """

        try:
            html = requests.get(self.URL_AVAILABILITY).text
        except requests.RequestException:
            return None

        data = json.loads(html.split("(", 1)[1][:-2])

        for line in data["answer"]["availability"]:
            if line["reference"] != model:
                continue


            availability = None
            for zone in line["metaZones"]:
                if zone["zone"] == "fr":
                    availability = zone["availability"]
                    break
            else:
                continue


            if availability == "unavailable":
                return False

            return True

        return False

    def stop(self):
        self._continue = False


class TaeminKimsuffi(plugin.TaeminPlugin):
    helper = {}

    MODEL = "160sk1"

    def __init__(self, taemin):
        super().__init__(taemin)
        self.thread = KimsuffiSearch(callback=self.on_new_availability, refresh=20)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()

    def on_new_availability(self, available):
        """ Each time we found a new kimsuffi server """

        if available:
            msg = "Server %s is available here %s" % (self.MODEL, URL)
        else:
            msg = "Server %s is no more available here %s" % (self.MODEL, URL)

        for chan in self.taemin.chans:
            self.privmsg(chan, msg)

if __name__ == "__main__":
    def _callback(available):
        print(available)

    KimsuffiSearch(_callback, refresh=5).start()
