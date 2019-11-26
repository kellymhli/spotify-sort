from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, jsonify
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

        session["user_id"] = user.user_id
        session["spotify_id"] = user.spotify_id
        session["logged_in"] = True
        return redirect("/playlists")
    else:
        return redirect("/register")


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
    session["user_id"] = user_id
    session["spotify_id"] = spotify_id
    session["logger_in"] = True

    return redirect("/playlists")


@app.route("/logout")
def logout():
    """Log user out of app."""

    # Drop user from session
    session["user_id"] = None
    session["spotify_id"] = None
    session["logged_in"] = False

    return redirect("/")


@app.route("/playlists")
def display_playlists():
    """Display a list of the user's playlist."""

    user = User.query.filter(User.user_id == session["user_id"]).one()

    # User user's spotify_id to get playlists
    playlists = Playlist.query.filter(Playlist.spotify_id == user.spotify_id)

    # List of bpms from 50-200 at 5bpm increments
    bpm_range = [bpm for bpm in range(50, 201, 5)]

    # List of valence from 0-1 at 0.2 increments
    valence_dict = {"None": None,
                    "Bleh": 0.2,
                    "Low": 0.4,
                    "Neutral": 0.6,
                    "Happy": 0.8,
                    "Euphoric": 1}

    # Get music keys
    keys = Key.query.all()

    return render_template("playlists2.html",
                           playlists=playlists,
                           bpm_range=bpm_range,
                           valence_dict=valence_dict,
                           keys=keys)


@app.route("/playlist/<string:playlist_id>")
def get_pl_tracks(playlist_id):
    """Display all the tracks of a given playlist_id."""

    playlist = Playlist.query.get(playlist_id)
    tracks = playlist.tracks
    return render_template("playlist_tracks.html", playlist=playlist, tracks=tracks)


@app.route("/playlist-tracks")
def return_pl_tracks():
    """Return playlist track object."""

    playlist_id = request.args.get('pl')
    playlist = Playlist.query.get(playlist_id)
    playlist_tracks = playlist.tracks
    tracks = []

    for track in playlist_tracks:
        tracks.append({
            "track_id" : track.track_id,
            "track_name" : track.track_name,
            "artist" : track.artist,
            "spotify_id" : track.spotify_id,
            "playlist_id" : track.playlist_id,
            "key" : track.key,
            "mode" : track.mode,
            "danceability" : track.danceability,
            "energy" : track.energy,
            "instrumentalness" : track.instrumentalness,
            "loudness" : track.loudness,
            "speechiness" : track.speechiness,
            "valence" : track.valence,
            "tempo" : track.tempo,
            "uri" : track.uri,
            "href" : track.href,
            "duration" : track.duration})
  
    return jsonify(tracks)


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


@app.route("/sort-playlists", methods=["GET"])
def sort_tracks():
    """Return a list of tracks with similar bpms."""

    playlists = []
    all_tracks = []
    bpm_tracks = []
    valence_tracks = []
    key_tracks = []
    matching_key_tracks = []

    # Get list of all selected playlists
    playlist_ids = request.args.getlist("playlist")

    # Get selected features
    bpm = request.args.get("bpm")
    valence = request.args.get("valence")
    key = request.args.get("key")

    if key != "None":
        keyname = Key.query.filter(Key.key_id == key).one()
        match_keys = MatchingKey.query.filter(MatchingKey.key_id == key).all()
    else:
        keyname = "None"

    # Get tracks of a playlist and append track to list
    for playlist_id in playlist_ids:
        playlist = Playlist.query.get(playlist_id)
        playlists.append(playlist)
        all_tracks.extend(playlist.tracks)
        # tracks = playlist.tracks
        # for track in tracks:
        #     all_tracks.append(track)

    for track in all_tracks:
        # Round track's bpm to nearest int
        # And check if it's +/- 3bmp from selected bpm
        if bpm != "None":
            bpm = int(bpm)
            if (bpm - 3) <= int(track.tempo) <= (bpm + 3):
                bpm_tracks.append(track)

        # Add tracks of desired valence to a list
        if valence != "None":
            valence = float(valence)
            if (valence - 0.1) <= track.valence <= (valence + 0.1):
                valence_tracks.append(track)

        if key != "None":
            # Create list of tracks of user selected key
            if int(track.key) == int(key):
                key_tracks.append(track)

            # Create a list of tracks with keys that pair well with user selected key
            if (int(track.key) == int(match_keys[0].matching_key)
                or int(track.key) == int(match_keys[1].matching_key)):
                    matching_key_tracks.append(track)


    # Get all tracks that match requirements
    sorted_tracks = set(bpm_tracks) & set(valence_tracks)

    return render_template("sorted-tracks.html",
                           bpm=bpm,
                           playlists=playlists,
                           bpm_tracks=bpm_tracks,
                           valence_tracks=valence_tracks,
                           keyname=keyname,
                           key_tracks=key_tracks,
                           matching_key_tracks=matching_key_tracks,
                           sorted_tracks=list(sorted_tracks))


@app.route("/new-playlist", methods=["GET"])
def display_new_playlist():
    """Display selected songs to that user would like to make a new playlist with."""

    # Make sure track only shows up once in the list
    track_ids = list(set(request.args.getlist("track")))
    tracks = []

    # Get all track object by track_id
    for track_id in track_ids:
        tracks.append(Track.query.get(track_id))

    return render_template("new_playlist.html", tracks=tracks)


@app.route("/add-playlist", methods=["POST"])
def add_playlist_to_db():
    """Add new playlist to database."""

    pl_name = request.form.get("pl_name")
    tracks = request.form.getlist("tracks[]")
    seed.add_playlist(session["spotify_id"], pl_name, tracks)

    return redirect("/playlists")


if __name__ == "__main__":

    # Needs to be true upon invoking DebugToolbarExtension
    app.debug = True
    # Make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(port=8888, host="0.0.0.0")