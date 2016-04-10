#!/usr/bin/env python2
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import requests
import romkan

class Transliterate(object):
    def __init__(self, word, alphabet):
        self.alphabets = {"hiragana": self._to_hiragana,
                          "katakana": self._to_katakana,
                          "ja": self._to_hiragana,
                          "romaji": self._to_romaji,
                          "hangul": self._to_hangul,
                          "ko": self._to_hangul,
                          "roman": self._to_roman}

        self.word = word
        self.alphabet = alphabet
        self.trans = None
        self.transliterate()

    def transliterate(self):
        self.trans = self.alphabets.get(self.alphabet, self._no_alphabet)()

    def _to_hiragana(self):
        return romkan.to_hiragana(self.word).encode("utf-8")

    def _to_katakana(self):
        return romkan.to_katakana(self.word).encode("utf-8")

    def _to_romaji(self):
        return romkan.to_roma(self.word.decode("utf-8"))

    def _no_alphabet(self):
        return self.word

    def _to_hangul(self):
        url = "http://www.kawa.net/works/hangul/hangul.cgi"
        try:
            html = requests.post(url, data={"query": self.word}).text
        except requests.exceptions.RequestException as err:
            print(err)
            return self.word
        soup = BeautifulSoup(html, 'html.parser')
        return soup.select("form font[face=GulimChe]").pop().text.encode("utf-8").strip()

    def _to_roman(self):
        url = "http://www.kawa.net/works/ajax/romanize/romanize.cgi"
        try:
            html = requests.post(url, data={"mode": "hangul", "q": self.word}).text
        except requests.exceptions.RequestException as err:
            print(err)
            return self.word
        soup = BeautifulSoup(html, 'html.parser')
        return "".join([child.attrs.get("title", " ") for child in soup.find_all("span")])

if __name__ == "__main__":
    print(Transliterate("tabe", "jazef").trans)
    print(Transliterate("にんじゃ", "romaji").trans)
    print(Transliterate("taemin", "hangul").trans)
    print(Transliterate("태민", "roman").trans)

