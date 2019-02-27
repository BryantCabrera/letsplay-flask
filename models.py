import datetime

from peewee import *

DATABASE = SqliteDatabase('letsplay.sqlite')

class User(Model):
    name = CharField()
    email = CharField()
    password = CharField()
    location = IntegerField()
    # member_since = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Boardgame(Model):
    title = CharField()
    designer = CharField()
    number_of_players_max = IntegerField()
    number_of_players_min = IntegerField()
    age_min = IntegerField()
    play_time_max = IntegerField()
    play_time_min = IntegerField()
    img_url = CharField()
    description = CharField()
    # created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class UserBoardgame(Model):
    user = ForeignKeyField(User, related_name='userboardgame')
    boardgame = ForeignKeyField(Boardgame, related_name='userboardgame')
    # joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Boardgame], safe=True)
    DATABASE.close()