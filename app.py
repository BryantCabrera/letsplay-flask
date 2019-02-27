# from flask import Flask
from flask import Flask, g, render_template, flash, redirect, url_for #updated for login

import config
import models
from resources.users import users_api
from resources.boardgames import boardgames_api
from resources.userboardgames import userboardgames_api
from flask_cors import CORS
# from flask_login import LoginManager
from flask_login import LoginManager, login_user, logout_user, login_required, current_user #updated for login
from flask_bcrypt import check_password_hash #for login

import models #for login

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
CORS(users_api, origins= ["http://localhost:3000"], supports_credentials=True)
CORS(boardgames_api, origins=["http://localhost:3000"], supports_credentials=True)

##manage pool connections to the database
@app.before_request
def before_request():
        """connect to the database before each request"""
        g.db = models.DATABASE
        g.db.connect()
        g.user=current_user

@app.after_request
def after_request(response):
    """Close the databased connection after each request"""
    g.db.close()
    return response

#registers blueprints in our app
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(boardgames_api, url_prefix='/api/v1')
app.register_blueprint(userboardgames_api, url_prefix='/api/v1')

#Routes
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)