"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, flash, request
from .models import DB, User, Tweet
from .twitter import add_update_user
from .prediction import predict_user


def get_user(username):
    return User.query.filter(User.name==username).first()


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
            n_tweets = add_update_user(username)
            if n_tweets == -1:
                flash('No such user!')
            elif n_tweets >= 0 and n_tweets < 20:
                User.query.filter(User.name==username).delete()
                DB.session.commit()
                flash('User has less than 20 tweets! Removed.')
            else:
                flash('User added with {} tweets.'.format(n_tweets))
        else:
            n_tweets = add_update_user(username)
            flash('User updated with {} new tweets.'.format(n_tweets))
        return render_template('base.html', title='Home',
                               users=User.query.order_by(User.name))

    @app.route('/user/<username>')
    def user(username):
        user = get_user(username)
        return render_template('user.html', title=username,
                               user=user)

    @app.route('/update')
    def update():
        update_string = ''
        for user in User.query.all():
            n_tweets = add_update_user(user.name)
            if n_tweets > 0:
                update_string = update_string + '<br>{} had {} new tweets.'.format(user.name,
                                                                                   n_tweets)
        flash('All users updated!' + update_string)
        return render_template('base.html', title='Home', 
                               users=User.query.order_by(User.name))

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home')

    return app