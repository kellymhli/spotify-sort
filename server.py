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
def homepage():
    """Homepage."""

    # Determine if user is logged in or not
    if session.get("user_id") != None:
        session["logged_in"] = True
    else:
        session["logged_in"] = False

    return render_template("homepage.html", 
                           logged_in=session["logged_in"])


@app.route("/login", methods=["GET"])
def login_page():
    """Render login page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """Log user into app."""

    # Get username and password from login page
    user_id = request.form.get("user_id")
    password = request.form.get("password")

    # Get user info from database
    user = User.query.get(user_id)

    if user != None:
        # Check that entered password matches user password in db
        # Log user into session
        correct_pass = user.password
        while password != correct_pass:
            password = request.form.get("password")
            # FLASH MESSAGE IF WRONG PASSWORD

        session["user_id"] = user.user_id
        session["logged_in"] = True
        return redirect("/playlists")
    else:
        return redirec("/register")


@app.route("/register", methods=["GET"])
def register_page():
    """Render register page."""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    """Register new user and store into db."""

    # Get all user information to be logged into db
    user_id = request.form.get("user_id")
    spotify_id = request.form.get("spotify_id")
    password = request.form.get("password")
    confirm_pass = request.form.get("confirm_pass")

    # Stay on page until password and confirmation passwords match
    while password != confirm_pass:
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_pass")

    # Get access token for Spotify oAuth
    access_token =  api.get_access_token(spotify_id) 

    # Add user and their playlists + tracks into db if new user
    if User.query.get(user_id) == None:
        seed.load_user(user_id, spotify_id, password, access_token)

    # Track user in session
    session['user_id'] = user_id
    session['logged_in'] = True

    return redirect("/playlists")


@app.route("/logout")
def logout():
    """Log user out of app."""

    # Drop user from session
    session["user_id"] = None
    session["logged_in"] = False

    return redirect("/")


@app.route("/playlists")
def display_playlists():
    """Display a list of the user's playlist."""

    user = User.query.filter(User.user_id == session["user_id"]).one()

    # User user's spotify_id to get playlists
    playlists = Playlist.query.filter(Playlist.spotify_id == user.spotify_id)

    return render_template("playlists3.html", playlists=playlists)


@app.route("/playlist/<string:playlist_id>")
def get_pl_tracks(playlist_id):
    """Display all the tracks of a given playlist_id."""

    playlist = Playlist.query.get(playlist_id)
    tracks = playlist.tracks
    return render_template("playlist-tracks.html", playlist=playlist, tracks=tracks)


@app.route("/tracks")
def display_tracks():
    """Display all user tracks."""

    user = User.query.filter(User.user_id == session["user_id"]).one()

    tracks = Track.query.filter(Track.spotify_id == user.spotify_id)

    return render_template("tracks.html", tracks=tracks)


@app.route("/tracks/<string:track_id>")
def display_pl_tracks(track_id):
    """Display deatils of a track given the track_id."""

    track_fts = Track.query.get(track_id)
    
    return render_template("track_features.html", track_fts=track_fts)


# @app.route("/bpm/<int:tempo>")
# def find_match():

#     # Query for all tracks of a given tempo (bpm)
#     return render_template("bpm_match.html", tracks=tracks)

#AJAX
    # bpm = request.args.get('bpm')
    # track = query for the tracks => get one
    # track_dict = {"track_name":track.track_name,
    #                 ""}

# @app.route("/playlists")
# def display_playlists():
#     """Display list of playlists to select and view."""

#     # username = session.get("user_id")
#     # print(username)

#     # # Get list of tuples of (playlist_id, pl_name)
#     # playlists = [playlist for playlist in db.session.query(Playlist.playlist_id, 
#     #              Playlist.pl_name).all()]

#     #a list of all Playlist objects in db that belong to logged in user
#     playlists_alt = Playlist.query.filter(Playlist.user_id==username)
#     print(playlists_alt)
#     # Get playlist + track_ids
#     all_playlist_tracks = PlaylistTrack.query

#     # key= playlist_id, value = [list of track_ids in playlist]
#     tracks_by_playlists = {}

#     for playlist in playlists:
#         # Query all tracks in a given playlist and addse to dictionary
#         playlist_tracks = all_playlist_tracks.filter(PlaylistTrack.playlist_id == playlist[0]).all()
#         tracks_by_playlists[playlist[0]] = playlist_tracks

#     # Get musical keys
#     keys = Key.query.all()

#     # Get all tracks in db
#     tracks = Track.query.all()

#     # List of bpms from 50-200 at 5bpm increments
#     bpm_range = [bpm for bpm in range(50, 201, 5)]

#     # List of valence from 0-1 at 0.2 increments
#     valence_dict = {"Depressed": 0.2, "Sad": 0.4, "Neutral": 0.6, "Happy": 0.8, "Euphoric": 1}


if __name__ == "__main__":

    # Needs to be true upon invoking DebugToolbarExtension
    app.debug = True 
    # Make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug 

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=8888, host="0.0.0.0")