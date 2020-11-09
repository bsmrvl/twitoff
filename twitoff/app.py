"""Main app/routing file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User, Tweet
from .tweets import USERS, TWEETS


def create_app():
    """Start app and load predefined users/tweets from twitoff.tweets"""

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        for user in USERS:
            DB.session.add(user)
        for tweet in TWEETS:
            DB.session.add(tweet)
        DB.session.commit()

        return render_template('base.html', title='home', 
                               users=User.query.order_by(User.name), 
                               tweets=Tweet.query.order_by(Tweet.id))

    return app