#!/usr/bin/env python2
# -*- coding: utf8 -*-

import requests
import random

class ImageSearch(object):
    URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, apicx, apikey):
        self.apicx = apicx
        self.apikey = apikey
 
        self.word = None
        self.html = None
        self.images = None
        self.image = None
        self.tiny = None

    def search(self, word):
        if isinstance(word, list) or not word.strip():
            self.word = random.choice(word)
        else:
            self.word = word

        self.html = self._get_json()
        self.images = self._get_images()
        self.image = self._get_image()
        self.tiny = self._url_to_tiny()

    def _get_json(self, rsz=10):
        data = {"cx": self.apicx,
                "searchType": "image",
                "key": self.apikey,
                "num": rsz,
                "q": self.word}
        try:
            request = requests.get(self.URL, params=data)
        except requests.exceptions.RequestException as err:
            return {}

        return request.json

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

def main():
    image = ImageSearch("", "")

if __name__ == "__main__":
    main()

