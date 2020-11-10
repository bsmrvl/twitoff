"""Retrieve tweets and users, then create embeddings to populate DB."""

from os import getenv
import spacy
import tweepy
from .models import DB, Tweet, User

nlp = spacy.load('my_model')
def vectorize_tweet(text):
    return nlp(text).vector

TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_API_KEY'), getenv('TWITTER_API_KEY_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

def add_update_user(username):
    try:
        twit_user = TWITTER.get_user(username)
        db_user = User.query.get(twit_user.id) or User(id=twit_user.id, name=username)
        DB.session.add(db_user)

        tweets = twit_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode='extended'
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorize_tweet(tweet.full_text))
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

        DB.session.commit()

    except Exception as e:
        print('Error processing{}: {}'.format(username, e))
        raise e