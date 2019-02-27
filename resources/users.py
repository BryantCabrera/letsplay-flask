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
        return jsonify({'users': [{'username': 'Bryant'}]})

    def post(self):
        args = self.reqparse.parse_args()
        print(args, ' this is args from UserList in users.py')
        user = models.User.create(**args)
        return jsonify({'users': [{'name': 'Bryant'}]})


class User(Resource):
    def get(self, id):
        return jsonify({'username': 'Bryant'})

    def put(self, id):
        return jsonify({'username': 'BryantCabrera'})

    def delete(self, id):
        return jsonify({'username': 'Bryant Cabrera deleted'})

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