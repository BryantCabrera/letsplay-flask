from flask import Flask

import config
import models
from resources.users import users_api
from resources.boardgames import boardgames_api
from resources.userboardgames import userboardgames_api
from flask_cors import CORS
from flask_login import LoginManager
login_manager = LoginManager()

app = Flask(__name__)

#sets up the login for our app
app.secret_key = config.SECRET_KEY
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

#CORS allows our React app to connect to our APIs
#supports_credentials=True allows us to send cookties back and forth
CORS(boardgames_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins= ["http://localhost:3000"], supports_credentials=True)

#registers blueprints in our app
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(boardgames_api, url_prefix='/api/v1')
app.register_blueprint(userboardgames_api, url_prefix='/api/v1')

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)