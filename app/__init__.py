from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_msearch import Search
import json, os

with open('config.json','r') as c:
    params=json.load(c)["params"]

db = SQLAlchemy()
search = Search()
login_manager = LoginManager()

def create_app():
    #create and configure the app
        
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    SESSION_TYPE="sqlalchemy"
    SESSION_SQLALCHEMY="sqlite:///../db.sqlite3"
    SESSION_PERMANENT=False

    search.init_app(app)

    app.secret_key = os.urandom(24)    
        
    from .blog import blog
    app.register_blueprint(blog)

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from .post import post
    app.register_blueprint(post, url_prefix="/post")

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to access this page"
    login_manager.login_message_category = "danger"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from . import models
    
    return app
