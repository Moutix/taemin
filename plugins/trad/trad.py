#!/usr/bin/env python2
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import requests

class Traduction(object):
    URL = "https://translate.google.com/"
    def __init__(self, word, language1, language2):
        self.word = word
        self.language1 = language1
        self.language2 = language2
        self.trad = word
        self.romaji = None
        self.html = self.get_html()
        self.translate()

    def get_html(self):
        data = {"sl": self.language1, "tl": self.language2, "js": "n", "ie": "UTF-8", "text": self.word}
        html = requests.post(self.URL, data=data).text
        return BeautifulSoup(html, 'html.parser')

    def translate(self):
        try:
            self.trad = self.html.find(id="result_box").span.string.encode("utf-8")
        except Exception:
            return
        try:
            self.romaji = self.html.find(id="res-translit").string.encode("utf-8")
        except Exception:
            return

if __name__ == "__main__":
    trad = Traduction("Tabe", "ja", "fr")
    print trad.romaji
    print trad.trad

