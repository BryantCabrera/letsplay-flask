import json

from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

from flask_login import login_user, logout_user, login_required, current_user

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

    #this is one way of incorporating marshal.  Including this marshal without decorater to demonstrate it's the same as with the decorater
    @login_required
    def get(self):
        users = [marshal(user, user_fields)
                   for user in models.User.select()]
        return {'users': users}

    #@marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            print(args, ' this is args from UserList in users.py')
            user = models.User.create_user(**args)
            login_user(user)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match!'
            }), 400)


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

    @login_required
    @marshal_with(user_fields)
    def get(self, id):
        return user_or_404(id)

    @login_required
    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(**args).where(models.User.id == id)
        query.execute()
        return (models.User.get(models.User.id == id), 200)

    @login_required
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