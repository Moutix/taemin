""" Quotation plugin """

import re

from taemin import database
from taemin import schema
from taemin import plugin
from .quotation_schema import Quotation

class TaeminQuotation(plugin.TaeminPlugin):
    helper = {"quote": "Quote un message. Usage: !quote add|show|suppress pseudo indice|nombre de quotes à supprimer(-indice supérieur)"}

    def on_pubmsg(self, msg):
        if msg.key != "quote":
            return

        chan = msg.chan.name

        random_func = database.db.random_func

        if msg.value == "":
            result = Quotation.select().where(Quotation.chan == msg.chan).order_by(random_func()).limit(1)
            for res in result:
                self.privmsg(chan, "%s - %s : %s" % (res.id, res.user.name, res.value))
            return

        kws = re.search(r'(?P<key>\w+)\s+(?P<user>\w+)(?:\s+)?(?P<limit>\d+)?(?:-)?(?P<uplimit>\d+)?', msg.value)
        if not kws:
            self.privmsg(chan, "Il est probable que vous ayez employé une mauvaise syntaxe. Un exemple : !quote add Potiron 8-12 ou !quote add Potiron 4")
            return


        kws = kws.groupdict()
        key = kws["key"]
        quote_user = kws["user"]
        quote_limit = int(kws["limit"] if kws["limit"] else 1)
        uplimit = int(kws["uplimit"]) - quote_limit + 1 if (kws["uplimit"] and (int(kws["uplimit"]) > quote_limit)) else 1


        if key == "add":
            user = self.get_user(quote_user)
            if not user:
                self.privmsg(chan, "Cet utilisateur n'existe pas")
                return

            quotes = self.prout(user, msg.chan, quote_limit, uplimit)
            if not quotes:
                self.privmsg(chan, "un probleme est survenu lors de l'enregistrement de la quote : Aucun message à enregistrer")
                return
            tosave = ""
            for quote in quotes:
                tosave = quote.message + "  " + tosave
            Quotation.create(user=user, chan=msg.chan, value=tosave)
            self.privmsg(chan, "La quote suivante : %s a bien été ajoutée" % tosave)
            return

        if key == "suppress":
            try:
                quote = Quotation.get(Quotation.id == quote_limit)
                if quote is not None:
                    quote.delete_instance()
                    self.privmsg(chan, "La quote numéro %s a bien été supprimée" % quote_limit)
                    return

            except Quotation.DoesNotExist:
                self.privmsg(chan, "Cette quote n'existe pas")
            return

        if key == "show":
            result = Quotation.select().where((Quotation.value.contains(quote_user)) & (Quotation.chan == msg.chan)).order_by(random_func()).limit(quote_limit)
            return

    def get_user(self, name):
        try:
            return schema.User.get(schema.User.name % name)
        except schema.User.DoesNotExist:
            return None


    def prout(self, user, chan, limit, uplimit):
        quotes = [quote for quote in (
            schema
            .Message
            .select()
            .where((schema.Message.user == user) & (schema.Message.chan == chan))
            .order_by(schema.Message.created_at.desc())
            .offset(limit - 1)
            .limit(uplimit))]

        if not quotes:
            self.privmsg(chan.name, "Aucune quote n'a été trouvée. Valeurs utilisées %s et %s et %s" % (limit, uplimit, user))
            return None

        return quotes
