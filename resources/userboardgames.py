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

    # def get(self):
    #     userboardgames = [marshal(userboardgame, userboardgame_fields)
    #                for userboardgame in models.UserBoardgame.select()]
    #     return {'userboardgames': userboardgames}
    @login_required
    def get(self):
        # test = models.Boardgame.select().join(models.UserBoardgame).join(models.User).where(models.User.id == current_user.id)
        # # args = self.reqparse.parse_args()
        # query = models.UserBoardgame.select().join(User).where(User.id == current_user.id)
        # print(query, ' this is query from userboardgames get')
        # print(str(current_user.id), 'args from get userbg')


        userboardgames = models.Boardgame.select().join(models.UserBoardgame).join(models.User).where(models.User.id == current_user.id)

        for boardgame in userboardgames:
            print(boardgame.title, ' this is test from userboardgames get')

        return userboardgames
        # userboardgames_ids = [marshal(userboardgame, userboardgame_fields)
        #            for userboardgame in models.UserBoardgame.select().where(models.UserBoardgame.user == str(current_user.id))]
        # for userboardgames_id in userboardgames_ids:
        #     print(userboardgames_id['boardgame'])
        # userboardgames = [for boardgame in models.Boardgame.select().where(models.Boardgame.id == for userboardgames_id in userboardgames_ids:userboardgames_ids['boardgame'])]
        
        # return {'userboardgames': userboardgames}

    # @login_required
    # @marshal_with(userboardgame_fields)
    # def post(self):
    #     args = self.reqparse.parse_args()
    #     print(args, ' this is args from UserBoardgameList in boardgames.py')
    #     userboardgame = models.UserBoardgame.create(**args)
    #     return userboardgame

    @login_required
    @marshal_with(userboardgame_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, ' this is args from UserBoardgameList post in userboardgames.py')
        userboardgame = models.UserBoardgame.create(user=args['user'], boardgame=args['boardgame'])
        # models.UserBoardgame.create(user=id, boardgame=boardgame_id);
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