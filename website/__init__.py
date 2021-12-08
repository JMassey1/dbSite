from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


def create_app():
    app = Flask(__name__)
    db = SQLAlchemy()

    DB_UNAME = "root"
    DB_PASS = "rootpas"
    DB_SERVER = "localhost"

    app.config['SECRET_KEY'] = 'this is a secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_UNAME}:{DB_PASS}@{DB_SERVER}/dbProject"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')




    return app

