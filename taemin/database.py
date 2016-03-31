#!/usr/bin/env python2
# -*- coding: utf8 -*-

from peewee import *
from taemin import conf
from playhouse.shortcuts import RetryOperationalError

class MySQLDB(RetryOperationalError, MySQLDatabase):
    pass

class DataBase(object):
    def __init__(self, type_, name, user="", password="", host="localhost", port=3306):
        self.type_ = type_
        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = self.init_db()
        class BaseModel(Model):
            class Meta:
                database = self.db
        self.basemodel = BaseModel

        if self.type_ == "mysql":
            self.random_func = fn.Rand
        else:
            self.random_func = fn.Random

    @classmethod
    def new_from_conf(cls):
        db_conf = conf.TaeminConf().config.get("database", {})
        return cls(db_conf.get("type", "mysql"),
                   name=db_conf.get("name", "/etc/taemin/taemin.db"),
                   user=db_conf.get("user", ""),
                   password=db_conf.get("password", ""),
                   host=db_conf.get("host", "localhost"))

    def init_db(self):
        available_db = {
            "sqlite": self._sqlite_db,
            "pgsql": self._postgre_db,
            "mysql": self._mysql_db
        }
        return available_db.get(self.type_, self._default_db)()

    def _sqlite_db(self):
        return SqliteDatabase(self.name)

    def _postgre_db(self):
        return PostgresqlDatabase(self.name, user=self.user, password=self.password, host=self.host)

    def _mysql_db(self):
        return MySQLDB(self.name, user=self.user, passwd=self.password, host=self.host, port=self.port)

    def _default_db(self):
        return SqliteDatabase(":memory")

db = DataBase.new_from_conf()

if __name__ == "__main__":
    database = DataBase("sqlite", "test.db")
    print database.db
