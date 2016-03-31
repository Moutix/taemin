#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import env, schema, plugin, courriel
from save_schema import Savedthings
import re
from peewee import fn
import requests
import mimetypes

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
        quotedmsg = self.get_message(quoteduser,msg.chan, kws.group(2))

        Savedthings.create(user = msg.user, content = quotedmsg)

        self.privmsg(chan, "Le contenu a bien été sauvegardé")

    def saveothers(self, msg, chan):
        if msg.value == "send":
            sauvegarde = Savedthings.select().where(Savedthings.user == msg.user)
            tablesauvegarde = self.parsecontent(sauvegarde)
            self.taemin.mailation.mailage(msg.chan.name, tablesauvegarde, msg.user)
            for line in tablesauvegarde:
                self.privmsg(chan, line)
            suppr = Savedthings.delete().where(Savedthings.user == msg.user)
            suppr.execute()
 
        else:
            self.savecontent(msg)

    def savecontent(self, msg):
        Savedthings.create(user = msg.user, content = msg.value)
    
    def parsecontent(self, sauvegarde):
        tableau = []
        for line in sauvegarde:
            if line.content.startswith("http"):
                self.privmsg("#gumi", "Je parse")
                r = mimetypes.guess_type(line.content)
                if r[0] == None:
                    #try:
                    re = requests.get(line.content).headers['Location']
                    #tableau.append(self.guesstype(re))
                    self.privmsg("#gumi", re)
                    #except:
                        #self.privmsg("#gumi", "Il y a une erreur sur la redirection")
                        #str = "<lien>"+line.content
                        #tableau.append(str)
                else:
                    tableau.append(self.guesstype(line.content))
            else:
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

    def guesstype(self, location):
        dico = {"image/png", "image/jpeg", "image/gif"}
        r = mimetypes.guess_type(location)
        self.privmsg("gumi", r[0])
        if r[0] in dicoimg:
            return "<image>"+location
        else:
            return "<lien>" +location

