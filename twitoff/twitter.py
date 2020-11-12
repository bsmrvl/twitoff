"""Functions for connecting to Twitter API, retrieving tweets, and vectorizing them."""

from os import getenv
import spacy
import tweepy
from .models import DB, Tweet, User


TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_API_KEY'), 
                                   getenv('TWITTER_API_KEY_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
nlp = spacy.load('my_model')


def add_update_user(username):
    """Attempt to add/update Twitter user, and return number of new tweets (-1 if no user exists)."""
    try:
        twit_user = TWITTER.get_user(username)
        db_user = User.query.get(twit_user.id) \
                  or User(id=twit_user.id, name=username)
        DB.session.add(db_user)

        tweets = twit_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode='extended',
            since_id=db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            t_text = tweet.full_text
            db_tweet = Tweet(
                id=tweet.id, 
                text=t_text, 
                vect=nlp(t_text).vector
            )
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

        DB.session.commit()
        
        if tweets:
            return len(tweets)
        else:
            return 0

    except:
        return -1