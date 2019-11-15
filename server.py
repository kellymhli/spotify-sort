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


# code snippets for login route
## get user id from a login form
# session["user_id"] = username
# print(session)

@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/login", methods=["GET"])
def login_page():
    """Render login page."""

    return render_template('login.html')


@app.route("/login", methods=["POST"])
def login():
    """Log user into app."""

    user_id = request.form.get('user_id')
    user = User.query.filter(User.user_id==user_id).one()
    session['user_id'] = user.user_id

    return redirect("/playlists")


@app.route("/auth")
def authorization():
    """Process username to authorize access to user Spotify data."""

    username = request.args.get("username")
    access_token =  api.get_access_token(username) # Get access token for Spotify oAuth
    seed.load_user(username, access_token)
 
    return redirect("/callback")


@app.route("/playlists")
def display_playlists():
    """Display a list of the user's playlist."""

    playlists = Playlist.query.filter(Playlist.user_id==session['user_id'])

    return render_template("playlists2.html", playlists=playlists)


@app.route("/playlist/<string:playlist_id>")
def get_pl_tracks(playlist_id):
    """Display all the tracks of a given playlist_id."""

    playlist = Playlist.query.get(playlist_id)
    tracks = playlist.tracks
    return render_template("tracks.html", tracks=tracks)


@app.route("/tracks/<string:track_id>")
def display_pl_tracks(track_id):
    """Display deatils of a track given the track_id."""

    track_fts = Track.query.get(track_id)
    
    return render_template("track_features.html", track_fts=track_fts)

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

#     return render_template("playlists.html", 
#                            playlists=playlists,
#                            tracks_by_playlists=tracks_by_playlists,
#                            keys=keys,
#                            tracks=tracks,
#                            bpm_range=bpm_range,
#                            valence_dict=valence_dict,
#                            playlists_alt=playlists_alt)


@app.route("/new-playlist")
def display_new_playlist():
    """Display list of selected songs that meet user selected requirements."""

    return render_template("new-playlist.html")


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