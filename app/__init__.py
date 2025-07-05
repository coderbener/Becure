from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()

def create_app():#factory function- instances
    app=Flask(__name__)#create an instance of Flask
    app.config['SECRET_KEY'] = os.urandom(24)#tampering, CSRF
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{os.environ.get('user')}:{os.environ.get('pass')}@{os.environ.get('host')}/{os.environ.get('datab')}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app