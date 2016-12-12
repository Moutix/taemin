#!/usr/bin/env python2
# -*- coding: utf8 -*-

import datetime

from peewee import fn, JOIN
from taemin import plugin, schema

class TaeminStats(plugin.TaeminPlugin):
    helper = {"stats": "Give the stats for the channel"}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        users = self.get_best_users(msg.chan)

        self.privmsg(msg.chan.name, "Top des plus bavards depuis 1 mois :")
        self.privmsg(
            msg.chan.name,
            ', '.join(
                "%s: %s" % (user.name, user.nb_messages)
                for user in users
            )
        )

        active_users = set((user.name for user in users if user.nb_messages > 0))

        away_users = [
            user.name
            for user in self.taemin.list_users(msg.chan)
            if user.name not in active_users
        ]

        if away_users:
            self.privmsg(
                msg.chan.name,
                "Personne connecté n'ayant pas parlé depuis plus d'un mois :"
            )
            self.privmsg(
                msg.chan.name,
                ", ".join(away_users)
            )
        else:
            self.privmsg(msg.chan.name, "Aucune personne inactive depuis 1 mois")

    @staticmethod
    def get_best_users(chan=None, since=datetime.timedelta(days=31), limit=None):
        """ Return the number of message by user """

        query = [schema.Message.created_at > datetime.datetime.now() - since]

        if chan:
            query.append(schema.Message.chan == chan)

        result = (schema.User
                  .select(schema.User.name, fn.COUNT(schema.Message.id).alias("nb_messages"))
                  .join(schema.Message, JOIN.LEFT_OUTER)
                  .where(*query)
                  .group_by(schema.User.name)
                  .order_by(fn.COUNT(schema.Message.id).desc()))

        if limit:
            result.limit(limit)

        return result


def main():
    print(list(TaeminStats.get_best_users(limit=5)))


if __name__ == "__main__":
    main()
