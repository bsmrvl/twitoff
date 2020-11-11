"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, request
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
        return render_template('base.html', title='Home',
                               users=User.query.order_by(User.name))

    @app.route('/newuser', methods=['POST'])
    def adduser():
        username = request.form.get('username')
        user = User.query.filter(User.name==username).first()
        if user is None:
            add_update_user(username)
            user = User.query.filter(User.name==username).first()
        return render_template('base.html', title='Home',
                               users=User.query.order_by(User.name))

    @app.route('/user/<username>')
    def user(username):
        user = User.query.filter(User.name==username).first()
        # if user is None:
        #     add_update_user(username)
        #     user = User.query.filter(User.name==username).first()
        return render_template('user.html', title=username,
                               user=user)

    @app.route('/update')
    def update():
        insert_example_users()
        return render_template('base.html', title='Home', 
                               users=User.query.order_by(User.name))

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home')

    return app

def insert_example_users():
    add_update_user('webdevMason')
    add_update_user('tylerthecreator')
    add_update_user('bensomer_ville')