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

    # Get list of tuples of (playlist_id, pl_name)
    playlists = [playlist for playlist in db.session.query(Playlist.playlist_id, 
                 Playlist.pl_name).all()]
    # Get playlist + track_ids
    all_playlist_tracks = PlaylistTrack.query

    tracks_by_playlists = {}
    for playlist in playlists:
        # Query all tracks in a given playlist and add to dictionary
        playlist_tracks = all_playlist_tracks.filter(PlaylistTrack.playlist_id == playlist[0]).all()
        tracks_by_playlists[playlist[0]] = playlist_tracks

    # Get musical keys
    keys = Key.query.all()

    # Get all tracks in db
    tracks = Track.query.all()

    return render_template("playlists.html", 
                           playlists=playlists,
                           tracks_by_playlists=tracks_by_playlists,
                           keys=keys,
                           tracks=tracks)


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