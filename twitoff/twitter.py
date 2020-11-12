"""Retrieve tweets and users, then create embeddings to populate DB."""

from os import getenv
import spacy
import tweepy
from .models import DB, Tweet, User


TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_API_KEY'), 
                                   getenv('TWITTER_API_KEY_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
nlp = spacy.load('my_model')


def add_update_user(username):
    """Attempt to add/update Twitter user, and return False if none exists."""
    
    try:
        twit_user = TWITTER.get_user(username)
        db_user = User.query.get(twit_user.id) or User(id=twit_user.id, name=username)
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
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=nlp(tweet.full_text).vector)
            already = Tweet.query.filter(Tweet.id == tweet.id).first() is not None
            if not already:
                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)

        DB.session.commit()
        
        if tweets:
            return len(tweets)
        else:
            return 0

    except:
        return -1