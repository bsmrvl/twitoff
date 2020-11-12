"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, flash, request
from .models import DB, User
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
        """Home page."""
        return render_template(
            'base.html',
            title='Home',
            users=User.query.order_by(User.name)
        )

    @app.route('/prediction', methods=['POST'])
    def predict():
        """Get form data and display prediction."""
        username0 = request.form.get('user1')
        username1 = request.form.get('user2')
        hypo_tweet = request.form.get('hypotweet')

        prediction, probas = predict_user(username0, username1, hypo_tweet)
        winner = username1 if prediction else username0
        loser = username0 if prediction else username1
        proba = round(probas[prediction]*100)

        return render_template(
            'prediction.html', 
            title='Prediction',
            winner=winner, loser=loser, tweet=hypo_tweet, proba=proba
        )

    @app.route('/newuser', methods=['POST'])
    def adduser():
        """Add or update tweets for specified user."""
        username = request.form.get('username')

        # Add.
        if User.query.filter(User.name==username).first() is None:
            n_tweets = add_update_user(username)
            if n_tweets == -1:
                flash(f"{username} doesn't exist!")
            elif n_tweets >= 0 and n_tweets < 20:
                User.query.filter(User.name==username).delete()
                DB.session.commit()
                flash(f'{username} has less than 20 tweets! Removed.')
            else:
                flash(f'{username} added, with {n_tweets} tweets.')

        # Update.
        else:
            n_tweets = add_update_user(username)
            flash(f'{username} updated, with {n_tweets} new tweets.')

        return render_template(
            'base.html', 
            title='Home',
            users=User.query.order_by(User.name)
        )

    @app.route('/user/<username>')
    def user(username):
        """Display list of tweets for specified user in our database."""
        user = User.query.filter(User.name==username).first()

        return render_template(
            'user.html', 
            title=username,
            user=user
        )

    @app.route('/update')
    def update():
        """Add new tweets for all users in our database."""
        update_string = ''
        for user in User.query.all():
            n_tweets = add_update_user(user.name)
            if n_tweets > 0:
                update_string = f'{update_string}<br>{user.name} had {n_tweets} new tweets.'
        flash('All users updated!' + update_string)

        return render_template(
            'base.html', 
            title='Home', 
            users=User.query.order_by(User.name)
        )

    @app.route('/reset')
    def reset():
        """Delete all users/tweets from our database."""
        DB.drop_all()
        DB.create_all()

        return render_template(
            'base.html', 
            title='Home'
        )

    return app