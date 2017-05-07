#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
import requests

class TaeminShareIm(plugin.TaeminPlugin):
    helper = {"share": "Upload an image on lut.im. Usage !share http://<url-img>"}
    _URL = "https://lut.im/"

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        image = self.upload_image(msg.value)

        if not image:
            self.privmsg(chan, self.helper[msg.key])
            return

        self.privmsg(chan, image)

    @classmethod
    def upload_image(cls, url):
        url = cls.realurl(url)
        if not url:
            return None

        data = {"lutim-file-url": url,
                "format": "json",
                "first-view": "0",
                "crypt": "0",
                "delete-day": "0"
               }
        try:
            res = requests.post(cls._URL, data=data, verify=False).json()
        except requests.RequestException:
            return None

        try:
            return "%s%s" % (cls._URL, res["msg"]["short"])
        except KeyError:
            return None

    @staticmethod
    def realurl(url):
        try:
            return requests.get(url).url
        except requests.exceptions.RequestException:
            return None

if __name__ == "__main__":
    print(TaeminShareIm.upload_image("http://www.aardwolf.com/images/mushclient-aardwolf-336.jpg"))
