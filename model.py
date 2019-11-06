from flask_sqlalchemy import SQLAlchemy

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

    # Set up relationships between tables
    # User can have many playlists
    playlists = db.relationship("Playlist",
                                backref="users")

    # User can have many tracks
    tracks = db.relationship("Track",
                             backref="users")

    def __repr__(self):
        """Provide helpful representation of user."""

        return f"<User id: {self.user_id} name: {self.display_name}>"


class Playlist(db.Model):
    """Playlist information."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pl_name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # Set up relationship between playlists and tracks
    # Many-to-many relationship, so pass through track_playlist class
    track_playlists = db.relationship("TrackPlaylist")
    tracks = db.relationship("Track",
                             secondary="track_playlists",
                             backref="playlists")

    def __repr__(self):
        """Provide useful information about a playlist."""

        return f"Playlist id: {self.playlist_id} name: {self.pl_name}"


class TrackPlaylist(db.Model):
    """Playlists that a track is found in."""

    __tablename__ = "track_playlists"

    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"), primary_key=True)
    track_id = db.Column(db.String(200), db.ForeignKey("tracks.track_id"))

    # Set up many-to-many relationship between playlists and tracks
    playlist = db.relationship("Playlist")
    track = db.relationship("Track")

    def __repr__(self):
        """Provide useful informaton about playlist and track relationship."""

        return f"<TrackPlaylist track: {self.track_id} playlist: {self.playlist_id}>"


class Track(db.Model):
    """Track information."""
    # https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

    __tablename__ = "tracks"

    track_id = db.Column(db.String(200), primary_key=True)
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
    artist = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"))

    # Set up relationship between tracks, track_playlists, and playlists
    track_playlists = db.relationship("TrackPlaylist")

    def __repr__(self):
        """Provide useful information about track."""

        return f"<Track id: {self.track_id} name: {self.name} key: {self.key}>"


class Key(db.Model):
    """All possible keys for tracks."""

    __tablename__ = "keys"

    key_id = db.Column(db.Integer, primary_key=True)
    key_name = db.Column(db.String(20))

    # Set up relationship between tracks and keys
    tracks = db.relationship("Track",
                             backref="keys")


class MatchingKey(db.Model):
    """Keys that pair well with the primary key of a track."""

    __tablename__ = "matching_keys"

    key_pair = db.Column(db.Integer, autoincrement=True, primary_key=True)
    key_id = db.Column(db.Integer, db.ForeignKey("keys.key_id"))
    matching_key = db.Column(db.Integer, db.ForeignKey("keys.key_id"))

    # Set up relationship between keys and matching keys
    # key = db.relationship("Key", db.foreign_keys=[matching_key], backref="matching_keys", db.foreign_keys=[key_id])
    key = db.relationship("Key", 
                          backref="matching_keys")

    def __repr__(self):
        """Provide useful information about track keys."""

        return f"<Keys key: {self.key_id} matching_key: {self.matching_key}>"


def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///spotify"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Running this module interactively will leave you in a 
    # state of being able to work with the db directly

    from server import app
    connect_to_db(app)
    print("Connected to DB.")