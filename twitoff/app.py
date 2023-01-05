from flask import Flask, render_template
from .models import DB, User, Tweet


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

    app_title = "Who Tweeted What?"

    @app.route("/test")
    def test():
        return f"<p>Another {app_title} page</p>"

    @app.route('/hola')
    def hola():
        return "Hola, Twitoff!"

    @app.route("/reset")
    def reset():
        # Drop all database tables
        DB.drop_all()
        # Recreate all database tables according to
        # the indicated schemas in models.py
        DB.create_all()
        return """The database has been reset.
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>"""

    @app.route("/populate")
    def populate():
        # Create two fake users in the DB
        james = User(id=1, username="James")
        ashley = User(id=2, username="Ashley")
        # Insert information into the DB
        DB.session.add(james)
        DB.session.add(ashley)

        # Create six (6) fake tweets in the DB
        tweet1 = Tweet(
            id=1, text="""We build an ice castle by hand every winter
            just by using water, icicles and a little magic.""", user=james)
        tweet2 = Tweet(
            id=2, text="Missing that warm summer weather right now.",
            user=ashley)
        tweet3 = Tweet(
            id=3, text="""Drinking hot cocoa during snowy days is
            my favorite thing.""", user=james)
        tweet4 = Tweet(
            id=4, text="""Today, the first snow of the year fell in my city.
            ❄️☃️ I really love seeing the snow fall! 😆""", user=james)
        tweet5 = Tweet(
            id=5, text="""I just want to escape to the 🌊 ocean.
            It brings me such a calm, relaxing peace that compares
            to nothing else in this world!""", user=ashley)
        tweet6 = Tweet(
            id=6, text="""Dreaming about taking a nap in a hammock
            strung between two palm trees.""", user=ashley)
        # Insert information into the DB
        DB.session.add(tweet1)
        DB.session.add(tweet2)
        DB.session.add(tweet3)
        DB.session.add(tweet4)
        DB.session.add(tweet5)
        DB.session.add(tweet6)

        # Save the changes made to the database
        DB.session.commit()

        return """Created some users.
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>"""

    # return our app object after attaching the routes to it
    return app
