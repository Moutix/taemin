from peewee import *
import datetime


class DataBase(object):
    def __init__(self, type_, name, user="", password="", host="localhost"):
        self.type_ = type_
        self.name = name
        self.user = user
        self.password = password
        self.host = host

        self.db = self.init_db()

        class BaseModel(Model):
            class Meta:
                database = self.db

        self.basemodel = BaseModel

    def init_db(self):
        if self.type_ == "sqlite":
            db = SqliteDatabase(self.name)
        elif self.type_ == "pgsql":
            db = PostgresqlDatabase(self.name, user=self.user, password=self.password, host=self.host)
        elif self.type_ == "mysql":
            db = MySQLDatabase(self.name, user=self.user, password=self.password, host=self.host)
        else:
            db = SqliteDatabase(":memory:")

if __name__ == "__main__":
    database = DataBase("sqlite", "test.db")
    print database.basemodel


