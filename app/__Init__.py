from flask import Flask,redirect,flash,render_template,jsonify,request, url_for
from app.database import *
import urllib.request
import os

from werkzeug.utils import secure_filename

from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from .config import Config

db = SQLAlchemy()
migrate =Migrate(db)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


#app.secret_key = "secret key"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()
    from app.users.views import users
    app.register_blueprint(users)
    from app.posts.views import posts
    app.register_blueprint(posts)
    from app.main.views import main
    app.register_blueprint(main)
    from app.errors.handlers import errors
    app.register_blueprint(errors)
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    return app
