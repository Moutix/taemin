#!/usr/bin/env python2
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import requests

class Traduction(object):
    _URL = "https://translate.google.com/"
    _LANGUAGES = []

    def __init__(self, word, src, dst, romaji=None):
        self.word = word
        self.src = src
        self.dst = dst
        self.romaji = romaji

    @classmethod
    def _get_html(cls, word, dst_language, src_language="auto"):
        data = {"sl": src_language,
                "tl": dst_language,
                "js": "n",
                "ie": "UTF-8",
                "text": word}

        html = requests.post(cls._URL, data=data).text

        return BeautifulSoup(html, 'html.parser')

    @classmethod
    def _get_trad_from_html(cls, html):
        trad = html.find(id="result_box")
        if not trad or not trad.span or not trad.span.string:
            return None

        return trad.span.string.encode("utf-8")

    @classmethod
    def _get_romaji_from_html(cls, html):
        romaji = html.find(id="res-translit")
        if not romaji or not romaji.string:
            return None

        return romaji.string.encode("utf-8")

    @classmethod
    def _get_src_language_from_html(cls, html):
        src_language = [value.get("value")
                        for value in html.select("#gt-sl option[selected]")
                        if value.get("value") != "auto"]

        if not src_language:
            return None
        return src_language[0]

    @classmethod
    def available_languages(cls):
        if not cls._LANGUAGES:
            cls._LANGUAGES = [value.get("value")
                              for value in cls._get_html("", "").select("#gt-sl option")
                              if value.get("value") != "separator"]

        return cls._LANGUAGES

    @classmethod
    def translate(cls, word, dst_language, src_language="auto"):
        html = cls._get_html(word, dst_language, src_language)

        return cls(cls._get_trad_from_html(html),
                   src_language,
                   dst_language,
                   cls._get_romaji_from_html(html))

def main():
    trad = Traduction.translate("c'est du français", "ja")
    print(trad.word)
    print(trad.romaji)
    print(trad.src)
    print(trad.dst)
    print(Traduction.available_languages())

if __name__ == "__main__":
    main()
