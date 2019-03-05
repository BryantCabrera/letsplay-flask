import datetime
import requests
import json

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

#local DATABASE
# DATABASE = SqliteDatabase('letsplay.sqlite') 

#Deployment Configurations
import os

from playhouse.db_url import connect

DATABASE = connect(os.environ.get('DATABASE_URL'))

class User(UserMixin, Model):
    name = CharField()
    email = CharField(unique = True)
    password = CharField()
    location = IntegerField(default=90210, null = True)
    img_url = CharField(default='https://i.imgur.com/KbicDVh.jpg', null = True)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, name, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email)
            ).get()
        except cls.DoesNotExist:
            user = cls(name=name, email=email)
            user.password = generate_password_hash(password)

            user.save()
            return user
        else:
            raise Exception("User with that email already exists!")

class Boardgame(Model):
    title = CharField()
    designer = CharField()
    number_of_players_max = IntegerField()
    number_of_players_min = IntegerField()
    play_time = IntegerField()
    img_url = CharField()
    description = TextField()

    class Meta:
        database = DATABASE

class UserBoardgame(Model):
    user = ForeignKeyField(User, related_name='userboardgame')
    boardgame = ForeignKeyField(Boardgame, related_name='userboardgame')

    class Meta:
        database = DATABASE

def populate():
    for i in range(1, 31):
        request = requests.get('https://bgg-json.azurewebsites.net/thing/{number}'.format(number=i))

        parsed_request = json.loads(request.text)

        Boardgame.create(title=parsed_request['name'],
            designer=parsed_request['designers'][0],
            number_of_players_max=parsed_request['maxPlayers'],
            number_of_players_min=parsed_request['minPlayers'],
            play_time=parsed_request['playingTime'],
            img_url=parsed_request['image'],
            description=parsed_request['description'])

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Boardgame, UserBoardgame], safe=True)
    # populate()
    DATABASE.close()