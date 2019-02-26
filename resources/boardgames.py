from flask import jsonify, Blueprint

from flask_restful import Resource, Api

import models

class BoardgameList(Resource):
    def get(self):
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