"""SQLAlchemy User and Tweet models for out database"""
from flask_sqlalchemy import SQLAlchemy

# Create a DB object from SQLAlchemy class
DB = SQLAlchemy()


# Make a User table using SQLAlchemy


class User(DB.Model):
    """Creates a User Table with SQlAlchemy"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column
    username = DB.Column(DB.String, nullable=False)
    # most recent tweet id
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"User: {self.username}"


class Tweet(DB.Model):
    """Creates a Table that keeps track of tweets for each user"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text column
    # allows for text, emojis and links
    text = DB.Column(DB.Unicode(300), nullable=False)
    # create a relationship between Users and a Tweets
    # store our word embeddings "vectorization"
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id column (foreign / secondary key)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)
    # create a whole list of tweets to be attached to the User
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return f"Tweet: {self.text}"
