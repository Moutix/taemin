#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from todo_schema import Todo
import re

class TaeminTodo(plugin.TaeminPlugin):
    helper = {"todo": "Things to do in taemin. Use !todo (add nom)|(del index)|(assign index user)|(user|pattern)"}

    REGEX = re.compile(r"^(\w+)\s+(.+)$")
    REGEX_ASSIGN = re.compile(r"^assign\s+(\d+)\s+(\S+).*?$")

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        kws = self.REGEX.search(msg.value)

        if kws and kws.group(1) == "add":
            self.add_todo(msg.chan, kws.group(2), msg.user)
            self.privmsg(chan, "Todo add: %s" % kws.group(2))
            return

        if kws and kws.group(1) == "del":
            todo = self.get_todo(kws.group(2))
            if not todo:
                self.privmsg(chan, "Aucun todo ne correspond")
                return

            self.privmsg(chan, "Todo supprimé: %s" % todo.message)
            todo.delete_instance()
            return

        kws = self.REGEX_ASSIGN.search(msg.value)
        if kws:
            todo = self.get_todo(kws.group(1))
            if not todo:
                self.privmsg(chan, "Aucun todo ne correspond")
                return

            user = self.taemin.get_user(kws.group(2))
            if not user:
                self.privmsg(chan, "Aucun utilisateur ne correspond")
                return

            todo.user = user
            todo.save()

            self.privmsg(chan, "Todo assigné à %s: %s" % (user.name, todo.message))
            return

        user = self.taemin.get_user(msg.value.strip())
        if user:
            todos = [todo for todo in self.get_todos(msg.chan, user=user)]
        else:
            todos = [todo for todo in self.get_todos(msg.chan, patern=msg.value.strip())]

        if not todos:
            self.privmsg(chan, "Rien à faire ;)")
            return

        for todo in todos:
            self.privmsg(chan, "#%s. [%s] %s" % (todo.id, todo.user.name, todo.message))

    @classmethod
    def add_todo(cls, chan, value, user):
        Todo.create(chan=chan, user=user, message=value)

    @classmethod
    def get_todos(cls, chan, user=None, patern="", limit=5):
        request = (Todo.chan == chan)
        if user:
            request = request & (Todo.user == user)
        if patern and patern.strip():
            request = request & (Todo.message.contains(patern))

        return (Todo.select()
                    .where(request)
                    .limit(limit))

    @classmethod
    def get_todo(cls, ident):
        try:
            int(ident)
        except ValueError:
            return None
        try:
            todo = Todo.get(id=ident)
        except Todo.DoesNotExist:
            return None
        return todo
