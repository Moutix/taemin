#!/usr/bin/env python2
#-*- coding: utf8 -*-

from taemin import database, schema
from peewee import *
import datetime

class Todo(database.db.basemodel):
    user = ForeignKeyField(schema.User, related_name='todos')
    chan = ForeignKeyField(schema.Chan, related_name='todos')
    message = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

Todo.create_table(True)
