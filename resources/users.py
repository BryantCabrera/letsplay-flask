from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

#what we want to send back when a user is called
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'location': fields.Integer,
    # 'member_since': fields.DateTime(dt_format='rfc822'),
}

def user_or_404(user_id):
    try:
        user = models.User.get(models.User.id == user_id)
    except models.User.DoesNotExist:
        abort(404)
    else:
        return user

class UserList(Resource):
    #this is the response to the client
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=False,
            help='No name provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'location',
            required=False,
            help='No location provided.',
            location=['form', 'json']
        )
        # self.reqparse.add_argument(
        #     'member_since',
        #     required=False,
        #     help='No date found.',
        #     location=['form', 'json']
        # )
        super().__init__()

    def get(self):
        users = [marshal(user, user_fields)
                   for user in models.User.select()]
        return {'users': users}

    @marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, ' this is args from UserList in users.py')
        user = models.User.create(**args)
        return user


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=False,
            help='No name provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'location',
            required=False,
            help='No location provided.',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(user_fields)
    def get(self, id):
        return user_or_404(id)

    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(**args).where(models.User.id == id)
        query.execute()
        return (models.User.get(models.User.id == id), 200)

    @marshal_with(user_fields)
    def delete(self, id):
        query = models.User.delete().where(models.User.id == id)
        query.execute()
        return 'This user resource was successfully deleted.'

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
api.add_resource(
    User,
    '/users/<int:id>',
    endpoint='user'
)