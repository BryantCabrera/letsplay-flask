from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)
from flask_login import login_required, current_user
import models

#what we want to send back when a user is called
userboardgame_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'boardgame': fields.String,
}

boardgame_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'designer': fields.String,
    'number_of_players_max': fields.Integer,
    'number_of_players_min': fields.Integer,
    'play_time': fields.Integer,
    'img_url': fields.String,
    'description': fields.String,
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
    @login_required
    def get(self):
        userboardgames = models.Boardgame.select().join(models.UserBoardgame).join(models.User).where(models.User.id == current_user.id)
        games = []
        for boardgame in userboardgames:
            games.append(marshal(boardgame, boardgame_fields))
        return games

    @login_required
    @marshal_with(userboardgame_fields)
    def post(self):
        args = self.reqparse.parse_args()
        userboardgame = models.UserBoardgame.create(user=args['user'], boardgame=args['boardgame'])
        # boardgame = models.Boardgame.select().where(models.Boardgame.id == int(args['boardgame']))
        # print(int(args['boardgame']), 'args[boardgame]')
        # print(marshal(boardgame, boardgame_fields), ' this is boardgame from userboardgames.py')
        # return marshal(boardgame, boardgame_fields)
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
    
    # @marshal_with(userboardgame_fields)
    def get(self, id):
        userboardgames = models.Boardgame.select().join(models.UserBoardgame).join(models.User).where(models.User.id == id)
        games = []
        for boardgame in userboardgames:
            games.append(marshal(boardgame, boardgame_fields))
        return games
        # return userboardgame_or_404(id)

    @login_required
    @marshal_with(userboardgame_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.UserBoardgame.update(**args).where(models.UserBoardgame.user_id == id)
        query.execute()
        return (models.UserBoardgame.get(models.UserBoardgame.user_id == id), 200)

    @login_required
    @marshal_with(userboardgame_fields)
    def delete(self, id):
        query = models.UserBoardgame.delete().where(models.UserBoardgame.user_id == id)
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