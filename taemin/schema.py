#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import env
from peewee import *
from playhouse.fields import ManyToManyField
import datetime

class Chan(env.db.basemodel):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

class User(env.db.basemodel):
    name = CharField()
    online = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)

class Connection(env.db.basemodel):
    user = ForeignKeyField(User, related_name='connections')
    chan = ForeignKeyField(Chan, related_name='connections')
    connected_at = DateTimeField(default=datetime.datetime.now)
    disconnected_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

class Message(env.db.basemodel):
    user = ForeignKeyField(User, related_name='messages')
    message = TextField()
    key = TextField(null=True)
    value = TextField(null=True)
    target = TextField(null=True)
    chan = ForeignKeyField(Chan, related_name='messages', null=True)
    highlights = ManyToManyField(User, related_name='hl')

    created_at = DateTimeField(default=datetime.datetime.now)

User.create_table(True)
Chan.create_table(True)
Message.create_table(True)
Connection.create_table(True)
UserMessage = Message.highlights.get_through_model()
UserMessage.create_table(True)
