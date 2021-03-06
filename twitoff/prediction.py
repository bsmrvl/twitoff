"""User prediction functions for Twitoff."""

import numpy as np 
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import nlp


def predict_user(username0, username1, hypo_tweet_text):
    """Predict user with logistic regression model, trained on vectorized tweets."""
    user0 = User.query.filter(User.name == username0).one()
    user1 = User.query.filter(User.name == username1).one()
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    vects = np.vstack([user0_vects, user1_vects])             # X
    labels = np.concatenate([np.zeros(len(user0.tweets)),     # y
                             np.ones(len(user1.tweets))])

    hypo_tweet_vect = nlp(hypo_tweet_text).vector
    hypo_tweet_vect = np.reshape(hypo_tweet_vect, (1, -1))

    model = LogisticRegression()
    model.fit(vects, labels)

    pred = int(model.predict(hypo_tweet_vect)[0])
    probas = model.predict_proba(hypo_tweet_vect)[0]

    return pred, probas