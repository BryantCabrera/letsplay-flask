import datetime
import requests
import json

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('letsplay.sqlite')

class User(UserMixin, Model):
    name = CharField()
    email = CharField(unique = True)
    password = CharField()
    location = IntegerField(null = True)
    img_url = CharField(default='./static/imgs/no_img.png', null = True)
    # member_since = DateTimeField(default=datetime.datetime.now)

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
    # age_min = IntegerField()
    # play_time_max = IntegerField()
    # play_time_min = IntegerField()
    play_time = IntegerField()
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

def populate():
    for i in range(35, 101):
        request = requests.get('https://bgg-json.azurewebsites.net/thing/{number}'.format(number=i))
        # request = requests.get('https://www.boardgamegeek.com/xmlapi2/thing/id={number}'.format(number=i))
        # print(json.loads(request.text)['image'])
        # print(json.loads(request.text))
        parsed_request = json.loads(request.text)
        # boardgame = {
        #     'title': parsed_request['name'],
        #     'designer': parsed_request['designers'][0],
        #     'number_of_players_max': parsed_request['maxPlayers'],
        #     'number_of_players_min': parsed_request['minPlayers'],
        #     # 'age_min'': parsed_request['name'],
        #     # 'play_time_max'': parsed_request['name'],
        #     'play_time': parsed_request['playingTime'],
        #     'img_url': parsed_request['image'],
        #     'description': parsed_request['description']
        # }
        # print(boardgame)
        Boardgame.create(title=parsed_request['name'],
            designer=parsed_request['designers'][0],
            number_of_players_max=parsed_request['maxPlayers'],
            number_of_players_min=parsed_request['minPlayers'],
            # 'age_min'=parsed_request['name'],
            # 'play_time_max'=parsed_request['name'],
            play_time=parsed_request['playingTime'],
            img_url=parsed_request['image'],
            description=parsed_request['description'])

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Boardgame], safe=True)
    populate()
    DATABASE.close()
