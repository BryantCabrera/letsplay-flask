from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

#what we want to send back when a user is called
userboardgame_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'boardgame': fields.String,
}

class UserBoardgameList(Resource):
    #this is the response to the client
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'user',
            required=True,
            help='No user provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'boardgame',
            required=False,
            help='No boardgame provided.',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        return jsonify({'userboardgame': [{'user': 'Bryant2', 'boardgame': 'Settlers of Catan'}]})

    def post(self):
        args = self.reqparse.parse_args()
        print(args, ' this is args from UserBoardgameList in boardgames.py')
        userboardgame = models.UserBoardgame.create(**args)
        return jsonify({'userboardgame': [{'user': 'Bryant2', 'boardgame': 'Settlers of Catan'}]})


class UserBoardgame(Resource):
    def get(self, id):
        return jsonify({'user': 'Bryant2', 'boardgame': 'Settlers of Catan'})

    def put(self, id):
        return jsonify({'user': 'Bryant3', 'boardgame': 'Settlers of Catan'})

    def delete(self, id):
        return jsonify({'user': 'Bryant3 deleted', 'boardgame': 'Settlers of Catan'})

userboardgames_api = Blueprint('resources.userboardgame', __name__)
api = Api(userboardgames_api)
api.add_resource(
    UserBoardgameList,
    '/userboardgames',
    endpoint='userboardgames'
)
api.add_resource(
    UserBoardgame,
    '/userboardgames/<int:id>',
    endpoint='userboardgame'
)