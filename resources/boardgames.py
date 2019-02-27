from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

#what we want to send back when a user is called
user_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'designer': fields.String,
    'number_of_players_max': fields.Integer,
    'number_of_players_min': fields.Integer,
    'age_min': fields.Integer,
    'play_time_max': fields.Integer,
    'play_time_min': fields.Integer,
    'img_url': fields.String,
    'description': fields.String,
}

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
        self.reqparse.add_argument(
            'age_min',
            required=False,
            help='No minimum age provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'play_time_max',
            required=True,
            help='No maximum playtime provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'play_time_min',
            required=True,
            help='No minimum playtime provided.',
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

    def get(self):
        return jsonify({'boardgame': [{'title': 'Settlers of Catan'}]})

    def post(self):
        args = self.reqparse.parse_args()
        print(args, ' this is args from BoardgameList in users.py')
        boardgame = models.Boardgame.create(**args)
        return jsonify({'boardgame': [{'title': 'Settlers of Catan'}]})


class Boardgame(Resource):
    def get(self, id):
        return jsonify({'title': 'Settlers of Catan'})

    def put(self, id):
        return jsonify({'title': 'Settlers of Catan: Cities & Knights'})

    def delete(self, id):
        return jsonify({'title': 'Settlers of Catan: Cities & Knights deleted'})

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