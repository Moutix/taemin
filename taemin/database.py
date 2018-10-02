""" Database model """

import peewee

from taemin import conf

class RetryOperationalError(object):

    def execute_sql(self, sql, params=None, commit=True):
        try:
            cursor = super(RetryOperationalError, self).execute_sql(
                sql, params, commit)
        except peewee.OperationalError:
            if not self.is_closed():
                self.close()
            with peewee.__exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        return cursor


class MySQLRetryDatabase(RetryOperationalError, peewee.MySQLDatabase):
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
        class BaseModel(peewee.Model):
            class Meta:
                database = self.db
        self.basemodel = BaseModel

        if self.type_ == "mysql":
            self.random_func = peewee.fn.Rand
        else:
            self.random_func = peewee.fn.Random

    @classmethod
    def new_from_conf(cls):
        db_conf = conf.get_config("taemin").get("database", {})
        return cls(db_conf.get("type", "sqlite"),
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
        return peewee.SqliteDatabase(self.name)

    def _postgre_db(self):
        return peewee.PostgresqlDatabase(self.name, user=self.user, password=self.password, host=self.host)

    def _mysql_db(self):
        return MySQLRetryDatabase(self.name, user=self.user, passwd=self.password, host=self.host, port=self.port)

    def _default_db(self):
        return peewee.SqliteDatabase(":memory")

db = DataBase.new_from_conf()

if __name__ == "__main__":
    database = DataBase("sqlite", "test.db")
    print(database.db)
