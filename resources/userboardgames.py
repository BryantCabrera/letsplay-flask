from flask import jsonify, Blueprint

from flask_restful import Resource, Api

import models

class UserBoardgameList(Resource):
    def get(self):
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
    '/userboardgame/<int:id>',
    endpoint='userboardgame'
)