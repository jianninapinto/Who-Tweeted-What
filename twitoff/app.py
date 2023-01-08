from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user


def create_app():
    # Initialize the app
    app = Flask(__name__)

    # Database Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Register the database with the app
    DB.init_app(app)

    # Create a 'route' that detects when a user accesses it
    # Attach the route to the 'app' object

    @app.route("/")
    def root():
        # Return page contents
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    @app.route("/reset")
    def reset():
        # Drop all database tables
        DB.drop_all()
        # Recreate all database tables according to
        # the indicated schemas in models.py
        DB.create_all()
        return render_template('base.html', title='Reset Database')


    @app.route("/update")
    def update():
        """Updates all users"""
        # Get list of usernames of all users
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Users Updated')

    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        
        username = username or request.values['user_name']

        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message =  f'User "{username}" has been successfully added!'

            tweets = User.query.filter(User.username==username).one().tweets

        except Exception as e:
            message = f'Error adding {username}: {e}'
            tweets = []

        return render_template('user.html', title=username, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():

        user0, user1 = sorted([request.values['user0'], request.values['user1']])
        hypo_tweet_text = request.values['tweet_text']

        if user0 == user1:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)

            # Get into the if statement if the prediction is user1
            if prediction:
                message = f'"{hypo_tweet_text}" is more likely to be said by {user1} than by {user0}.'
            else:
                message = f'"{hypo_tweet_text}" is more likely to be said by {user0} than by {user1}.'
                
        return render_template('prediction.html', title='Prediction', message=message)    
        
    # return our app object after attaching the routes to it
    return app
