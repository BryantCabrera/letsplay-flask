from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)
from flask_login import login_required
import models

#what we want to send back when a user is called
userboardgame_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'boardgame': fields.String,
}

def userboardgame_or_404(userboardgame_id):
    try:
        userboardgame = models.UserBoardgame.get(models.UserBoardgame.id == userboardgame_id)
    except models.UserBoardgame.DoesNotExist:
        abort(404)
    else:
        return userboardgame

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

    #this is one way of incorporating marshal.  Including this marshal without decorater to demonstrate it's the same as with the decorater

    def get(self):
        userboardgames = [marshal(userboardgame, userboardgame_fields)
                   for userboardgame in models.UserBoardgame.select()]
        return {'userboardgames': userboardgames}

    @login_required
    @marshal_with(userboardgame_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, ' this is args from UserBoardgameList in boardgames.py')
        userboardgame = models.UserBoardgame.create(**args)
        return userboardgame


class UserBoardgame(Resource):
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
    
    @marshal_with(userboardgame_fields)
    def get(self, id):
        return userboardgame_or_404(id)

    @login_required
    @marshal_with(userboardgame_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.UserBoardgame.update(**args).where(models.UserBoardgame.id == id)
        query.execute()
        return (models.UserBoardgame.get(models.UserBoardgame.id == id), 200)

    @login_required
    @marshal_with(userboardgame_fields)
    def delete(self, id):
        query = models.UserBoardgame.delete().where(models.UserBoardgame.id == id)
        query.execute()
        return 'This userboardgame resource join was successfully deleted.'

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