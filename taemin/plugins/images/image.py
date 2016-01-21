#!/usr/bin/env python2
# -*- coding: utf8 -*-

import requests
import random

class ImageSearch(object):
    URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, conf, word=""):
        self.conf = conf
        self.word = word
        if not word.strip():
            self.word = random.choice(self.conf.get("ImageSearch", []))

        self.html = self._get_json()
        self.images = self._get_images()
        self.image = self._get_image()
        self.tiny = self._url_to_tiny()

    def _get_json(self, rsz=10):
        data = {"cx": self.conf.get("googleApi", {}).get("CX"),
                "searchType": "image",
                "key": self.conf.get("googleApi", {}).get("APIKEY"),
                "num": rsz,
                "q": self.word}
        try:
            r = requests.get(self.URL, params=data)
        except requests.exceptions.RequestException as err:
            return {}

        return r.json

    def _get_images(self):
        images = []

        for image in self.html.get("items", []):
            images.append(image.get("link", ""))

        return images

    def _get_image(self):
        return random.choice(self.images)

    def _url_to_tiny(self):
        try:
            tinyurl = requests.get("http://tinyurl.com/api-create.php", params={"url": self.image}).text
        except requests.exceptions.RequestException as err:
            return "Requests Error: %s" % err
        return tinyurl

if __name__ == "__main__":
    print ImageSearch({}).tiny
    print ImageSearch({}, "taemin").tiny

