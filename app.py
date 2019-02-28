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
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for) #for login

# import models #for login

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
# CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

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
#combines POST & GET requests
# @app.route('/register', methods=('GET', 'POST'))
# def register(self):
#     form = self.reqparse.parse_args() 
#     ##this if statement handles the post request
#     if form.validate_on_submit():
#         ##just returns true or false
#         flash('Yay you registered', 'success')
#         models.User.create_user(
#             username=form['username'], #getting from form's property called "username"
#             email=form['email'],
#             password=form['password']
#         )
#         return form
#     ##the response fo the GET request
#     ##inject the form as variable form into this view
#     return form

# @app.route('/login', methods=('GET', 'POST'))
# def login():
#     print(current_user, ' this is current_user from /login')
#     print(' this is request')
#     form = self.reqparse.parse_args()
#     print(form, 'this is form')
#     ##handles the POST request
#     if form.validate_on_submit():
#         try:
#             # user = models.User.get(models.User.email == form.email.data)
#             user = models.User.get(models.User.email == form['email'])
#         except models.DoesNotExist:
#             flash('Your email or password doesn\'t match', 'error')
#         else:
#             if check_password_hash(user.password, form['password']):
#                 ##login our user / create our session
#                 login_user(user)
#                 print('You have successfully logged in.')
#                 return user

#             else:
#                 flash('Your email or password doesn\'t match', 'error')
#     return form

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)