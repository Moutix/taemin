#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
from image import ImageSearch
from taemin import env, schema, plugin
from schema_image import Image
from peewee import fn

class TaeminImage(plugin.TaeminPlugin):
    helper = {"donne": "Recherche sur google image",
              "give": "Recherche sur google image",
              "keep": "Sauvegarde l'image. Usage : !keep name",
              "image": "Recherche une image parmis les sauvegardées",
              "remove_image": "Supprime une image sauvegardé. Usage: !remove_image id"}

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.confapi = env.conf.get("googleApi", {})
        self.confimage = env.conf.get("ImageSearch", {})
        self.image = ImageSearch(self.confapi.get("CX"), self.confapi.get("APIKEY"))

    def on_pubmsg(self, msg):
        chan = msg.chan.name

        if msg.key == "donne" or msg.key == "give":
            self.image.search(msg.value)
            self.privmsg(chan, self.image.tiny)
            return

        if msg.key == "keep":
            if msg.value == "":
                self.privmsg(chan, self.helper[msg.key])
                return

            if not self.image.image:
                self.privmsg(chan, "Aucune image en mémoire")
                return

            self.store(self.image, msg.chan, msg.value)
            self.privmsg(chan, "Image store: %s" % self.image.image)
            return

        if msg.key == "image":
            image = self.search_image(msg.value, msg.chan)
            if not image:
                self.privmsg(chan, "Aucune image ne correspond")
                return

            self.privmsg(chan, "[#%s: %s] %s: %s" % (image.id, image.name, image.word, image.image))

        if msg.key == "remove_image":
            try:
                id = int(msg.value)
            except:
                self.privmsg(chan, self.helper[msg.key])
                return

            image = self.destroy_image(msg.value, msg.chan)
            if not image:
                self.privmsg(chan, "Aucune image ne correspond")
                return

            self.privmsg(chan, "Image supprimé: [#%s: %s] %s" % (image.id, image.name, image.image))


        for word in self.confimage.keys():
            if re.compile("^.*" + word + ".*$").match(msg.message.lower()):
                self.image.search(self.confimage[word])
                self.privmsg(chan, self.image.tiny)

    def on_privmsg(self, msg):
        source = msg.user.name

        if msg.key == "donne" or msg.key == "give":
            self.image.search(msg.value)
            self.privmsg(source, self.image.tiny)

        for word in self.confimage.keys():
            if re.compile("^.*" + word + ".*$").match(msg.message.lower()):
                self.image.search(self.confimage[word])
                self.privmsg(source, self.image.tiny)

    def store(self, image, chan, name=""):
        Image.create(chan=chan, name=name, image=image.image, word=image.word, tiny=image.tiny)

    def search_image(self, name, chan):
        try:
            return Image.select().where((Image.name.contains(name)) & (Image.chan == chan)).order_by(env.db.random_func()).get()
        except Image.DoesNotExist:
            return None

    def destroy_image(self, id, chan):
        try:
            image = Image.get(id=id, chan=chan)
        except Image.DoesNotExist:
            return None

        image.delete_instance()
        return image


def main():
    print TaeminImage().image

if __name__ == "__name__":
    main()


