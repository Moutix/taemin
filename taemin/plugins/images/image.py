#!/usr/bin/env python2
# -*- coding: utf8 -*-

import random
import requests

class GoogleError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

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

        try:
            self.html = self._get_json()
        except GoogleError as err:
            self.html = None
            self.image = str(err)
            self.tiny = str(err)

        if self.html:
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
            request = requests.get(self.URL, params=data).json()
        except requests.exceptions.RequestException as err:
            raise GoogleError(err)

        if request.get("error"):
            raise GoogleError(request["error"].get("message"))

        return request

    def _get_images(self):
        images = []

        for image in self.html.get("items", []):
            images.append(image.get("link", ""))

        return images

    def _get_image(self):
        if not self.images:
            return "Aucun résultat"
        return random.choice(self.images)

    def _url_to_tiny(self):
        try:
            tinyurl = requests.get("http://tinyurl.com/api-create.php", params={"url": self.image}).text
        except requests.exceptions.RequestException as err:
            return "Requests Error: %s" % err
        return tinyurl

def main():
    APIKEY = "AIzaSyBZc32pq-zq99lybE7IyOl-NEd8aKcWB6I"
    CX = "007167590149092953870:rztyz-auexq"
    image = ImageSearch(CX, APIKEY)
    image.search("taemin")
    print(image.images)
    print(image.image)

if __name__ == "__main__":
    main()
