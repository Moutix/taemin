#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import schema, plugin
from save_schema import Savedthings
import re

class TaeminSave(plugin.TaeminPlugin):
    helper = {"save": "Sauvegarde du contenu. Usage: !save lien/texte or !save quote user number or !save send"}

    def on_pubmsg(self, msg):
        if msg.key != "save":
            return

        chan = msg.chan.name

        if msg.value == "":
            self.privmsg(chan, "Veuillez préciser le contenu à sauvegarder")
            return

        kws = re.search('quote\s+(\w+)\s+(\d+)', msg.value)
        if kws == None:
            self.saveothers(msg, chan)
            return

        quoteduser = self.get_user(kws.group(1))
        quotedmsg = self.get_message(quoteduser,msg.chan, int(kws.group(2)))

        Savedthings.create(user = msg.user, content = quotedmsg.message)

        self.privmsg(chan, "Le contenu a bien été sauvegardé")

    def saveothers(self, msg, chan):
        if msg.value == "send":
            sauvegarde = Savedthings.select().where(Savedthings.user == msg.user)
            tablesauvegarde = self.parsecontent(sauvegarde)
            self.taemin.mailation.mailage(msg.chan.name, tablesauvegarde, msg.user)
            suppr = Savedthings.delete().where(Savedthings.user == msg.user)
            suppr.execute()
 
        else:
            self.savecontent(msg)

    def savecontent(self, msg):
        Savedthings.create(user = msg.user, content = msg.value)

    def parsecontent(self, sauvegarde):
        tableau = []
        for line in sauvegarde:
            tableau.append(line.content)
        return tableau
    
   
    def get_message(self, user, chan, limit=1):
        quotes = [quote for quote in schema.Message.select().where((schema.Message.user == user) & (schema.Message.chan == chan)).order_by(schema.Message.created_at.desc()).offset(limit - 1).limit(1)]
        if not quotes:
            return None
        else:
            return quotes[0]

    def get_user(self, name):
        try:
            return schema.User.get(schema.User.name % name)
        except schema.User.DoesNotExist:
            #Il faudrait que je loggue un truc la quand meme...
            return None
