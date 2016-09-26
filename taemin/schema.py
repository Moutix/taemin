#!/usr/bin/env python2
# -*- coding: utf8 -*-

import datetime
import requests
import re

from playhouse.fields import ManyToManyField, AESEncryptedField
from peewee import *
from bs4 import BeautifulSoup, SoupStrainer

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

        true_url, title, content_type = cls.info_from_url(url)

        if not true_url:
            return None

        try:
            return cls.get(cls.url == true_url)
        except cls.DoesNotExist:
            pass

        return cls.create(url=true_url, title=title, type=content_type)

    @classmethod
    def info_from_url(cls, url):
        """
            Get true url, title and content_type form an url

            :param str url: The URL to requests

            :Example:
            >>> Link.info_from_url("https://google.com")
            (u'https://www.google.fr/', 'Google', 'text/html')
        """

        try:
            res = requests.get(url, stream=True, timeout=5)
        except requests.RequestException:
            return None, None, None

        if "content-type" in res.headers:
            content_type = res.headers["content-type"].split(";")[0]
        else:
            content_type = None

        if content_type == "text/html":
            title = cls.get_title(cls.get_head_dom(res))
        else:
            title = None

        res.close()

        return res.url, title, content_type


    @staticmethod
    def get_head_dom(res):
        dom = []
        for line in res.iter_lines():
            dom.append(line)
            if re.match(r".*</\s*head\s*>", line, flags=re.IGNORECASE):
                break

        return '\n'.join(dom)

    @classmethod
    def search(cls, query):
        return cls.select().where(
            (cls.title.contains(query)) |
            (cls.tags.contains(query)) |
            (cls.url.contains(query))
        )

    @staticmethod
    def get_title(html):
        """
            Get the title element from a HTML document

            :param str html: The html to parse

            :Example:

            >>> Link.get_title("xxxx<title>Title</title>xxxx")
            'Title'

            >>> print(Link.get_title("xxxx<>Title</title>xxxx"))
            None
        """
        bs = BeautifulSoup(html, 'html.parser', parse_only=SoupStrainer('title'))

        title = bs.find("title")
        if not title:
            return None

        if not title.string:
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
    message = AESEncryptedField(conf.get_config("taemin").get("aes_password", "banane"))
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()

