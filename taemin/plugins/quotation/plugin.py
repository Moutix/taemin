#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import env, schema
from quotation_schema import Quotation
import re
from peewee import fn

class TaeminQuotation(object):
    helper = {"quote": "Quote un message. Usage: !quote add|show pseudo indice"}

    def __init__(self, taemin):
        self.taemin = taemin 

    def on_pubmsg(self, serv, msg):
        if msg.key != "quote":
            return

        chan = msg.chan.name 

        if env.db.type_ == "mysql":
            random_func = fn.Rand
        else:
            random_func = fn.Random

        if msg.value == "":
            result = Quotation.select().where(Quotation.chan == msg.chan).order_by(random_func()).limit(1)
            for res in result:
                serv.privmsg(chan, "%s - %s : %s" % (res.id, res.user.name, res.value))
            return

        kws = re.search('(\w+)\s+(\w+)\s+(\d+)', msg.value)
        if kws == None:  
            serv.privmsg(chan, "Utilisation : !quote add/suppress pseudo  indice")
            return

        key = kws.group(1)
        quote_user = kws.group(2)
        quote_limit = int(kws.group(3))

        if key == "add":
            user = self.get_user(quote_user)
            if not user:
                serv.privmsg(chan, "Cet utilisateur n'existe pas")
                return

            quote = self.get_message(user, msg.chan, quote_limit)
            if not quote:
                serv.privmsg(chan, "Aucune quote ne correspond")
                return
            Quotation.create(user=user, chan=msg.chan, value=quote.message)
            serv.privmsg(chan, "La quote suivante : %s a bien été ajoutée" % quote.message)
            return

        if key == "suppress":
            try:
                quote = Quotation.get(Quotation.id == quote_limit)
                if quote is not None:
                    quote.delete_instance()
                    serv.privmsg(chan, "La quote numéro %s a bien été supprimé" % quote_limit)
                    return
            except:
                serv.privmsg(chan, "Cette quote n'existe pas")
            return

        if key == "show":
           
            result = Quotation.select().where((Quotation.value.contains(quote_user)) & (Quotation.chan == msg.chan)).order_by(random_func()).limit(quote_limit)
            for res in result:
                serv.privmsg(chan, "%s - %s : %s" % (res.id, res.user.name, res.value))
            return

    def get_user(self, name):
        try:
            return schema.User.get(schema.User.name % name)
        except schema.User.DoesNotExist:
            return None

    def get_message(self, user, chan, limit=1):
        quotes = [quote for quote in schema.Message.select().where((schema.Message.user == user) & (schema.Message.chan == chan)).order_by(schema.Message.created_at.desc()).offset(limit - 1).limit(1)]
        if not quotes:
            return None
        else:
            return quotes[0]

