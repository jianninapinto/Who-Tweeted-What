from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user


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

    @app.route("/populate")
    def populate():
        # Create two fake users in the DB
        add_or_update_user('BarackObama')
        add_or_update_user('elonmusk')
        add_or_update_user('justinbieber')
        add_or_update_user('rihanna')
        add_or_update_user('Cristiano')
        add_or_update_user('taylorswift13')
        add_or_update_user('KimKardashian')
        add_or_update_user('NASA')
        add_or_update_user('BillGates')
        add_or_update_user('Oprah')

        # Save the changes we just made to the database
        # DB.session.commit()

        return render_template('base.html', title='Populate Database')

    @app.route("/update")
    def update():
        """Updates all users"""
        # Get list of usernames of all users
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Users Updated')
        
    # return our app object after attaching the routes to it
    return app
