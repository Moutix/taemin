#!/usr/bin/env python2
#-*- coding: utf8 -*-

from taemin import env, schema
from peewee import *
import datetime

class Feed(env.db.basemodel):
    name = TextField()
    url = TextField()
    regex = TextField(null=True)
    conf = BooleanField(default=True)
    chan = ForeignKeyField(schema.Chan, related_name='feed', null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

class FeedEntry(env.db.basemodel):
    chan = ForeignKeyField(schema.Chan, related_name='feed_entries')
    feed = ForeignKeyField(Feed, related_name='entries')
    title = TextField()
    link = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

Feed.create_table(True)
FeedEntry.create_table(True)
