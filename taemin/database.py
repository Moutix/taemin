from peewee import *
import datetime
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

    def init_db(self):
        if self.type_ == "sqlite":
            db = SqliteDatabase(self.name)
        elif self.type_ == "pgsql":
            db = PostgresqlDatabase(self.name, user=self.user, password=self.password, host=self.host)
        elif self.type_ == "mysql":
            db = MySQLDB(self.name, user=self.user, passwd=self.password, host=self.host, port=self.port)
        else:
            db = SqliteDatabase(":memory:")
        return db


if __name__ == "__main__":
    database = DataBase("sqlite", "test.db")
    print database.db


