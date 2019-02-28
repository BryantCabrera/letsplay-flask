from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)
from flask_login import login_required
import models

#what we want to send back when a user is called
boardgame_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'designer': fields.String,
    'number_of_players_max': fields.Integer,
    'number_of_players_min': fields.Integer,
    # 'age_min': fields.Integer,
    # 'play_time_max': fields.Integer,
    # 'play_time_min': fields.Integer,
    'play_time': fields.Integer,
    'img_url': fields.String,
    'description': fields.String,
}

def boardgame_or_404(boardgame_id):
    try:
        boardgame = models.Boardgame.get(models.Boardgame.id == boardgame_id)
    except models.Boardgame.DoesNotExist:
        abort(404)
    else:
        return boardgame

class BoardgameList(Resource):
    #this is the response to the client
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No title provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'designer',
            required=False,
            help='No designer provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'number_of_players_max',
            required=True,
            help='No maximum number of players provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'number_of_players_min',
            required=True,
            help='No minimum number of players provided.',
            location=['form', 'json']
        )
        # self.reqparse.add_argument(
        #     'age_min',
        #     required=False,
        #     help='No minimum age provided.',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'play_time_max',
        #     required=True,
        #     help='No maximum playtime provided.',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'play_time_min',
        #     required=True,
        #     help='No minimum playtime provided.',
        #     location=['form', 'json']
        # )
        self.reqparse.add_argument(
            'play_time',
            required=True,
            help='No playtime provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'img_url',
            required=True,
            help='No image url provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'description',
            required=True,
            help='No description provided.',
            location=['form', 'json']
        )
        super().__init__()

    #this is one way of incorporating marshal.  Including this marshal without decorater to demonstrate it's the same as with the decorater
    def get(self):
        boardgames = [marshal(boardgame, boardgame_fields)
                   for boardgame in models.Boardgame.select()]
        return {'boardgames': boardgames}

    @login_required
    @marshal_with(boardgame_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, ' this is args from BoardgameList in boardgames.py')
        boardgame = models.Boardgame.create(**args)
        return boardgame


class Boardgame(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No title provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'designer',
            required=False,
            help='No designer provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'number_of_players_max',
            required=True,
            help='No maximum number of players provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'number_of_players_min',
            required=True,
            help='No minimum number of players provided.',
            location=['form', 'json']
        )
        # self.reqparse.add_argument(
        #     'age_min',
        #     required=False,
        #     help='No minimum age provided.',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'play_time_max',
        #     required=True,
        #     help='No maximum playtime provided.',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'play_time_min',
        #     required=True,
        #     help='No minimum playtime provided.',
        #     location=['form', 'json']
        # )
        self.reqparse.add_argument(
            'play_time',
            required=True,
            help='No playtime provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'img_url',
            required=True,
            help='No image url provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'description',
            required=True,
            help='No description provided.',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(boardgame_fields)
    def get(self, id):
        return boardgame_or_404(id)

    @login_required
    @marshal_with(boardgame_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Boardgame.update(**args).where(models.Boardgame.id == id)
        query.execute()
        return (models.Boardgame.get(models.Boardgame.id == id), 200)

    @login_required
    @marshal_with(boardgame_fields)
    def delete(self, id):
        query = models.Boardgame.delete().where(models.Boardgame.id == id)
        query.execute()
        return 'This boardgame resource was successfully deleted.'

boardgames_api = Blueprint('resources.boardgames', __name__)
api = Api(boardgames_api)
api.add_resource(
    BoardgameList,
    '/boardgames',
    endpoint='boardgames'
)
api.add_resource(
    Boardgame,
    '/boardgames/<int:id>',
    endpoint='boardgame'
)