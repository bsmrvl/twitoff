"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, flash, request
from .models import DB, User, Tweet
from .twitter import add_update_user
from .prediction import predict_user


def create_app():
    app = Flask(__name__)
    app.secret_key = getenv('APP_KEY_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home',
                               users=User.query.order_by(User.name))

    @app.route('/prediction', methods=['POST'])
    def predict():
        username1 = request.form.get('user1')
        username2 = request.form.get('user2')
        hypo_tweet = request.form.get('hypotweet')

        # def retry():
        #     return render_template('base.html', title='Home',
        #                            users=User.query.order_by(User.name))

        # if username1 == username2:
        #     flash("Users must be different!")
        #     return retry()
        # elif not hypo_tweet:
        #     flash("Hypothetical tweet can't be empty.")
        #     return retry()
        # else:
        prediction, probas = predict_user(username1, username2, hypo_tweet)
        winner = username2 if prediction else username1
        loser = username1 if prediction else username2
        proba = round(probas[prediction]*100)
        return render_template('prediction.html', title='Prediction',
                                winner=winner, loser=loser, tweet=hypo_tweet, proba=proba)

    @app.route('/newuser', methods=['POST'])
    def adduser():
        username = request.form.get('username')
        if get_user(username) is None:
            exists = add_update_user(username)
            if not exists:
                flash('No such user!')
            else:
                flash('User added!')
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
        flash('Users added!')
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