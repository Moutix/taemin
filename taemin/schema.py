#!/usr/bin/env python2
# -*- coding: utf8 -*-

import datetime
import requests

from playhouse.fields import ManyToManyField, AESEncryptedField
from peewee import *
from bs4 import BeautifulSoup

from taemin import database, conf


class Chan(database.db.basemodel):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

class User(database.db.basemodel):
    name = CharField()
    online = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)

class Link(database.db.basemodel):
    url = TextField()
    title = TextField(null=True)
    type = TextField(null=True)
    tags = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def new_from_url(cls, url):
        if not url:
            return None

        try:
            html = requests.get(url)
        except requests.RequestException:
            return None

        try:
            return cls.get(cls.url == html.url)
        except cls.DoesNotExist:
            pass

        try:
            title = cls._get_title(html.text)
        except TypeError:
            title = None

        return cls.create(url=html.url, title=title, type=html.headers["content-type"])

    @classmethod
    def search(cls, query):
        return cls.select().where(
            (cls.title.contains(query)) |
            (cls.tags.contains(query)) |
            (cls.url.contains(query))
        )

    @staticmethod
    def _get_title(html):
        bs = BeautifulSoup(html, 'html.parser')

        title = bs.find("title")
        if not title:
            return None

        return title.string.strip().replace('\n', ' ').encode("utf-8")


class Connection(database.db.basemodel):
    user = ForeignKeyField(User, related_name='connections')
    chan = ForeignKeyField(Chan, related_name='connections')
    connected_at = DateTimeField(default=datetime.datetime.now)
    disconnected_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

class Message(database.db.basemodel):
    user = ForeignKeyField(User, related_name='messages')
    message = AESEncryptedField(conf.TaeminConf().config["database"].get("aes_password", "banane"))
    key = TextField(null=True)
    value = TextField(null=True)
    target = TextField(null=True)
    chan = ForeignKeyField(Chan, related_name='messages', null=True)
    link = ForeignKeyField(Link, related_name='messages', null=True, on_delete='SET NULL')
    highlights = ManyToManyField(User, related_name='hl')

    created_at = DateTimeField(default=datetime.datetime.now)

class Mail(database.db.basemodel):
    user = ForeignKeyField(User, related_name='mail')
    mail = TextField()
    created_at = DateTimeField(default = datetime.datetime.now)

User.create_table(True)
Chan.create_table(True)
Link.create_table(True)
Message.create_table(True)
Connection.create_table(True)
UserMessage = Message.highlights.get_through_model()
UserMessage.create_table(True)
Mail.create_table(True)
