from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session
from flask_debugtoolbar import DebugToolbarExtension
import api, seed
from model import User, Playlist, PlaylistTrack, Track, Key, MatchingKey, connect_to_db, db

app = Flask(__name__)
app.secret_key = "ILIKEWIGGLINGTOMUSIC"

# Raise error when an undefined variable is used in Jinja2
# rather than failing silently
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/auth")
def authorization():
    """Process username to authorize access to user Spotify data."""

    username = request.args.get("username")
    access_token =  api.get_access_token(username) # Get access token for Spotify oAuth
    seed.load_user(username, access_token)
    return redirect("/callback")


@app.route("/playlists")
def display_playlists():
    """Display list of playlists to select and view."""

    playlists = db.session.query(Playlist.pl_name).all()
    return render_template("playlists.html")

@app.route("/callback")
def callback():
    """Callback page after authorization through spotify."""

    return render_template("callback.html")


if __name__ == "__main__":

    # Needs to be true upon invoking DebugToolbarExtension
    app.debug = True 
    # Make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug 

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=8888, host="0.0.0.0")