from flask_sqlalchemy import flask_sqlalchemy

# Create connection to PostgreSQL database through Flask-SQLAlchemy library. 
# Contains the session object.
db = SQLAlchemy()

# Model definitions

class User(db.Model):
    """Spotify user information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    display_name = db.Column(db.String(50))
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"))
    url = db.Column(db.String(200))
    img_url = db.Column(db.String(200))


class Playlist(db.Model):
    """Playlist information."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pl_name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


class Track(db.Model):
    """Track information."""
    # https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

    __tablename__ = "tracks"

    track_id = db.Column(db.String(200))
    name = db.Column(db.String(300))
    key = db.Column(db.Integer)
    mode = db.Column(db.Integer)  # Major/minor mode
    danceability = db.Column(db.Float)  # How suitable track if for dancing
    energy = db.Column(db.Float)  # Intensity and activity
    instrumentalness = db.Column(db.Float) 
    loudness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    valence = db.Column(db.Float)  # Positiveness of track
    tempo = db.Column(db.Float)  # BPM
    uri = db.Column(db.String(200))
    href = db.Column(db.String(300))


class MatchingKey(db.Model):
    """Keys that pair well with the primary key of a track."""

    __tablename__ = "matching_keys"

    key_id = db.Column(db.Integer, db.ForeignKey("tracks.key"))
    matching_key = db.Column(db.Integer)



