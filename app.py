from flask import Flask

import config
import models
from resources.users import users_api
from resources.boardgames import boardgames_api
from resources.userboardgames import userboardgames_api

app = Flask(__name__)
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(boardgames_api, url_prefix='/api/v1')
app.register_blueprint(userboardgames_api, url_prefix='/api/v1')

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)