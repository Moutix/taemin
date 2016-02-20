#!/usr/bin/env python2
# -*- coding: utf8 -*-

import requests
import urllib

class AlloFilm(object):
    def __init__(self, id, name, year, picture, director):
        self.year = year
        self.name = name
        self.director = director
        self.id = id
        self.picture = picture
        self.link = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % self.id

    def __str__(self):
        return "<Film-%s %s (%s)>" % (self.id, self.name, self.year)

    def __repr__(self):
        return "<Film-%s %s (%s)>" % (self.id, self.name, self.year)

class AlloLocalization(object):
    def __init__(self, id, name, code):
        self.id = id
        self.name = name
        self.code = code

    def __str__(self):
        return "<Localization-%s %s (%s)" % (self.id, self.name, self.code)

    def __repr__(self):
        return "<Localization-%s %s (%s)" % (self.id, self.name, self.code)

class TaeminCine(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, msg):
        pass


    def get_film(self, film):
        res = self.get_films(film)
        if res:
            return res[0]
        return None

    def get_films(self, film):
        try:
            res = requests.get("http://essearch.allocine.net/fr/autocomplete", params={"q": film})
        except requests.RequestException:
            return []

        return [film for film in self.films_generator(res.json)]

    def films_generator(self, raw_result):
        for film in raw_result:
            director = None
            year = None
            for meta in film.get("metadata", []):
                if meta.get("property") == "director":
                    director = meta.get("value", "").encode("utf-8")
                elif meta.get("property") == "productionyear":
                    year = meta.get("value", "").encode("utf-8")

            yield AlloFilm(film.get("id"),
                           film.get("title2", "").encode("utf-8"),
                           year,
                           film.get("poster", "").encode("utf-8"),
                           director)

    def get_localization(self, localization):
        res = self.get_localizations(localization)
        if res:
            return res[0]
        return None

    def get_localizations(self, localization):
        try:
            res = requests.get("http://www.allocine.fr/_/localization/%s" % urllib.quote(localization))
        except requests.RequestException:
            return []

        return [localization for localization in self.localizations_generator(res.json)]

    def localizations_generator(self, raw_result):
        for localization in raw_result:
            yield AlloLocalization(localization.get("id"),
                                   localization.get("name", "").encode("utf-8"),
                                   localization.get("zip_code", "").encode("utf-8"))

    def get_seances(self, film, localization):
        if isinstance(film, str):
            film = self.get_film(film)
        if isinstance(localization, str):
            localization = self.get_localization(localization)
        try:
            res = requests.get("http://www.allocine.fr/_/showtimes/movie-%s/near-%s/" % (film.id, localization.id))
        except requests.RequestException:
            return []

        return res.json

def main():
    cine = TaeminCine(None)

    print cine.get_films("deadpool")
    print cine.get_localizations("paris")

    print cine.get_seances("deadpool", "antony")


if __name__ == "__main__":
    main()

