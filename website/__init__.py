from flask import Flask
from flask_login import LoginManager, UserMixin
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.automap import automap_base
from os import path

engine = create_engine(r'sqlite:///boptunes.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base = automap_base()


# User model inheritance for UserMixin
class User(Base, UserMixin):
    __tablename__ = 'Users'

    def get_id(self):
        return (self.User_ID)

    def isArtist(self):
        with engine.connect() as conn:
            results = conn.execute(
                text("SELECT COUNT(1) FROM Artists WHERE User_ID = :User_ID"),
                {"User_ID": self.User_ID}
            )
        temp = results.first()[0]
        return bool(temp)


Base.prepare(engine, reflect=True)

session = Session(engine)


def create_app():
    app = Flask(__name__)

    DB_NAME = "boptunes.db"

    app.config['SECRET_KEY'] = 'this is a secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(User_ID):
        # with engine.connect() as conn:
        #     results = conn.execute(
        #         text("SELECT User_ID FROM Users WHERE username = :username"),
        #         {"username": username}
        #     )
        return session.query(User).get(int(User_ID))

    return app

