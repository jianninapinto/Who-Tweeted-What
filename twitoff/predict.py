"""Prediction of users based on tweets"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_username, user1_username, hypo_tweet_text):
    """
    Determines and returns which user is more likely to say a given tweet.
    Example run: predict_user("elonmusk", "BarackObama", "No one is born hating
    another person because of the color of his skin")
    Returns a 0 (user0_name: "elonmusk") or a 1 (user1_name: "BarackObama")
    """
    # Grab user from the database
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Grab tweet vectors or word embeddings from each tweet for each user
    user0_vects = np.array([ tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack tweet vects to get one np array. (The X matrix)
    vects = np.vstack([user0_vects, user1_vects])

    # Concatenate the labels of 0 or 1 for each tweet. (The y target )
    labels = np.concatenate([np.zeros(user0_vects.shape[0]), np.ones(user1_vects.shape[0])])

    # Instantiate and fit the model with our X's == vects & our y's == labels
    log_reg = LogisticRegression().fit(vects, labels)

    # Vectorize the hypothetical tweet text to pass into .predict()
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)


    return log_reg.predict(hypo_tweet_vect)

