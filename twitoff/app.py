"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template
from .models import DB, User, Tweet
# from .tweets import USERS, TWEETS
from .twitter import add_update_user


def create_app():
    """Start app and load predefined users/tweets from twitoff.tweets"""

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='home',
                               users=User.query.order_by(User.name), 
                               tweets=Tweet.query.order_by(Tweet.id))

    @app.route('/update')
    def update():
        insert_example_users()
        return render_template('base.html', title='home', 
                               users=User.query.order_by(User.name), 
                               tweets=Tweet.query.order_by(Tweet.id))

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='home')

    return app

def insert_example_users():
    add_update_user('bensomer_ville')
    add_update_user('elonmusk')