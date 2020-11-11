"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, flash, request
from .models import DB, User, Tweet
from .twitter import add_update_user


def create_app():
    app = Flask(__name__)
    app.secret_key = getenv('APP_KEY_SECRET')
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
        if get_user(username) is None:
            exists = add_update_user(username)
            if not exists:
                flash('No such user.')
        else:
            flash('User already here!')
        return render_template('base.html', title='Home',
                               users=User.query.order_by(User.name))

    @app.route('/user/<username>')
    def user(username):
        user = get_user(username)
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


def get_user(username):
    return User.query.filter(User.name==username).first()


def insert_example_users():
    add_update_user('webdevMason')
    add_update_user('tylerthecreator')
    add_update_user('bensomer_ville')