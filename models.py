import datetime

from peewee import *

DATABASE = SqliteDatabase('letsplay.sqlite')

class User(Model):
    name = CharField()
    email = CharField()
    password = CharField()
    member_since = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()