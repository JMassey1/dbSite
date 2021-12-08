from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

#db = __init__.db


class User(db.Model, UserMixin):
    usrID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(150))
    Library = db.relationship('Library')


class Listeners(db.Model):
    pass


class Artists(db.Model):
    pass


class Library(db.Model):
    libID = db.Column(db.Integer, primary_key=True)
    usrID = db.Column(db.Integer, db.ForeignKey('user.usrID'))


class Song(db.Model):
    songID = db.Column(db.Integer, primary_key=True)
    songName = db.Column(db.String(50))
    songGenre = db.Column(db.String(15))


class Album(db.Model):
    albumID = db.Column(db.Integer, primary_key=True)
    albumName = db.Column(db.String(50))
    albumGenre = db.Column(db.String(15))
