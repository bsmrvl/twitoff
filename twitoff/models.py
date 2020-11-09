"""SQLAlchemy models and utility functions for Twitoff Application"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """User Table - SQLAlchemy syntax"""

    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """Tweets Table - SQLAlchemy syntax"""

    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)