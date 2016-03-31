#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import database
from peewee import *
from playhouse.fields import ManyToManyField
import datetime


class Chan(database.db.basemodel):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

class User(database.db.basemodel):
    name = CharField()
    online = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)

class Connection(database.db.basemodel):
    user = ForeignKeyField(User, related_name='connections')
    chan = ForeignKeyField(Chan, related_name='connections')
    connected_at = DateTimeField(default=datetime.datetime.now)
    disconnected_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

class Message(database.db.basemodel):
    user = ForeignKeyField(User, related_name='messages')
    message = TextField()
    key = TextField(null=True)
    value = TextField(null=True)
    target = TextField(null=True)
    chan = ForeignKeyField(Chan, related_name='messages', null=True)
    highlights = ManyToManyField(User, related_name='hl')

    created_at = DateTimeField(default=datetime.datetime.now)

class Mail(database.db.basemodel):
    user = ForeignKeyField(User, related_name='mail')
    mail = TextField()
    created_at = DateTimeField(default = datetime.datetime.now)

User.create_table(True)
Chan.create_table(True)
Message.create_table(True)
Connection.create_table(True)
UserMessage = Message.highlights.get_through_model()
UserMessage.create_table(True)
Mail.create_table(True)
