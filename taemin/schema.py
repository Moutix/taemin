#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
import datetime
import requests
import logging

import peewee
from bs4 import BeautifulSoup, SoupStrainer

from taemin import database, conf

LOGGER = logging.getLogger(__name__)


class Chan(database.db.basemodel):
    name = peewee.CharField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

class User(database.db.basemodel):
    name = peewee.CharField()
    online = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

class Link(database.db.basemodel):
    url = peewee.TextField()
    title = peewee.TextField(null=True)
    type = peewee.TextField(null=True)
    tags = peewee.TextField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

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

        try:
            return cls.create(url=true_url, title=title, type=content_type)
        except:
            LOGGER.exception("cannot save link from url %s with title %s", url, title)

        return None

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
        except (requests.RequestException, UnicodeError):
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
        if res.encoding is None:
            res.encoding = 'utf-8'

        dom = []
        for line in res.iter_lines(decode_unicode=True):
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

        return title.string.strip().replace('\n', ' ')


class Connection(database.db.basemodel):
    user = peewee.ForeignKeyField(User, related_name='connections')
    chan = peewee.ForeignKeyField(Chan, related_name='connections')
    connected_at = peewee.DateTimeField(default=datetime.datetime.now)
    disconnected_at = peewee.DateTimeField(default=datetime.datetime.now)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

class Message(database.db.basemodel):
    user = peewee.ForeignKeyField(User, related_name='messages')
    #message = AESEncryptedField(conf.get_config("taemin").get("aes_password", "banane").encode("utf-8"))
    message = peewee.TextField()
    key = peewee.TextField(null=True)
    value = peewee.TextField(null=True)
    target = peewee.TextField(null=True)
    chan = peewee.ForeignKeyField(Chan, related_name='messages', null=True)
    link = peewee.ForeignKeyField(Link, related_name='messages', null=True, on_delete='SET NULL')
    highlights = peewee.ManyToManyField(User, backref='hl')

    created_at = peewee.DateTimeField(default=datetime.datetime.now)

class Mail(database.db.basemodel):
    user = peewee.ForeignKeyField(User, related_name='mail')
    mail = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

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
