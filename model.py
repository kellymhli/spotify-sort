from flask_sqlalchemy import SQLAlchemy
import api

# Create connection to PostgreSQL database through Flask-SQLAlchemy library.
# Contains the session object.
db = SQLAlchemy()

# Model definitions

class User(db.Model):
    """Spotify user information."""

    __tablename__ = "users"

    user_id = db.Column(db.String(100), primary_key=True, unique=True)
    spotify_id = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    token = db.Column(db.String(500))

    # Set up relationships between tables
    # User can have many playlists
    playlists = db.relationship("Playlist",
                                backref="user")

    # User can have many tracks
    tracks = db.relationship("Track",
                             backref="user")

    def __repr__(self):
        """Provide helpful representation of user."""

        return f"<User id: {self.user_id} spotify: {self.spotify_id}>"


class Playlist(db.Model):
    """Playlist information."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.String(200), primary_key=True)
    pl_name = db.Column(db.String(50))
    spotify_id = db.Column(db.String, db.ForeignKey("users.spotify_id"))

    # Set up relationship between playlists and tracks
    # Many-to-many relationship, so pass through playlist_track class
    playlist_tracks = db.relationship("PlaylistTrack")
    tracks = db.relationship("Track",
                             secondary="playlist_tracks",
                             backref="playlists")

    def __repr__(self):
        """Provide useful information about a playlist."""

        return f"Playlist id: {self.playlist_id} name: {self.pl_name}"


class PlaylistTrack(db.Model):
    """Playlists that a track is found in."""

    __tablename__ = "playlist_tracks"

    playList_track_pair = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.String(200), db.ForeignKey("playlists.playlist_id"), primary_key=True)
    track_id = db.Column(db.String(200), db.ForeignKey("tracks.track_id"))

    # Set up many-to-many relationship between playlists and tracks
    playlist = db.relationship("Playlist")
    track = db.relationship("Track")

    def __repr__(self):
        """Provide useful informaton about playlist and track relationship."""

        return f"<PlaylistTrack track: {self.track_id} playlist: {self.playlist_id}>"


class Track(db.Model):
    """Track information."""
    # https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

    __tablename__ = "tracks"

    track_id = db.Column(db.String(200), primary_key=True)
    track_name = db.Column(db.String(300))
    artist = db.Column(db.String(100))
    spotify_id = db.Column(db.String(100), db.ForeignKey("users.spotify_id"))
    playlist_id = db.Column(db.String(200), db.ForeignKey("playlists.playlist_id"))
    key = db.Column(db.Integer, db.ForeignKey("keys.key_id"))
    mode = db.Column(db.Integer)  # Major/minor mode
    danceability = db.Column(db.Float)  # How suitable track if for dancing
    energy = db.Column(db.Float)  # Intensity and activity
    instrumentalness = db.Column(db.Float)
    loudness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    valence = db.Column(db.Float)  # Positiveness of track
    tempo = db.Column(db.Float)  # BPM
    uri = db.Column(db.String(1000))
    href = db.Column(db.String(300))
    duration = db.Column(db.Integer)

    # Set up relationship between tracks, playlist_tracks, and playlists
    playlist_tracks = db.relationship("PlaylistTrack")

    def __repr__(self):
        """Provide useful information about track."""

        return f"<Track id: {self.track_id} name: {self.track_name} key: {self.key}>"


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
    key_id = db.Column(db.Integer)  #, db.ForeignKey("keys.key_id"))
    matching_key = db.Column(db.Integer, db.ForeignKey("keys.key_id"))

    # Set up relationship between keys and matching keys
    #key = db.relationship("Key", db.foreign_keys=[matching_key], backref="matching_keys", db.foreign_keys=[key_id])
    key = db.relationship("Key",
                          backref="matching_keys")

    def __repr__(self):
        """Provide useful information about track keys."""

        return f"<Keys key: {self.key_id} matching_key: {self.matching_key}>"


def example_data():
    """Create sample data for testing."""

    # Empty out existing data incase this is run multiple times
    User.query.delete()
    Playlist.query.delete()
    PlaylistTrack.query.delete()
    Track.query.delete()
    Key.query.delete()
    MatchingKey.query.delete()

    user = User(user_id="kels", spotify_id="kelspot",
                password="wiggle", token="sometokenvalue")
    
    db.session.add(user)

    pl1 = Playlist(playlist_id="pl1", pl_name="First Playlist", spotify_id="kelspot")
    pl2 = Playlist(playlist_id="pl2", pl_name="Second Playlist", spotify_id="kelspot")

    db.session.add_all([ pl1, pl2])

    k1 = Key(key_id=1, key_name="C")
    k2 = Key(key_id=2, key_name="D")
    k3 = Key(key_id=3, key_name="E")

    db.session.add_all([k1, k2, k3])

    mk1 = MatchingKey(key_id=1, matching_key=2)
    mk2 = MatchingKey(key_id=2, matching_key=3)
    mk3 = MatchingKey(key_id=1, matching_key=1)

    db.session.add_all([mk1, mk2, mk3])

    t1 = Track(track_id="t1", track_name="Track 1", spotify_id="kelspot",
               playlist_id="pl1", key=1, tempo=121, valence=0.7)
    t2 = Track(track_id="t2", track_name="Track 2", spotify_id="kelspot",
               playlist_id="pl1", key=1, tempo=123, valence=0.5)
    t3 = Track(track_id="t3", track_name="Track 3", spotify_id="kelspot",
               playlist_id="pl1", key=2, tempo=119, valence=0.6)
    t4 = Track(track_id="t4", track_name="Track 4", spotify_id="kelspot",
               playlist_id="pl2", key=2, tempo=120, valence=0.63)
    t5 = Track(track_id="t5", track_name="Track 5", spotify_id="kelspot",
               playlist_id="pl2", key=3, tempo=119, valence=0.4)

    db.session.add_all([t1, t2, t3, t4, t5])

    pt1 = PlaylistTrack(playlist_id='pl1', track_id="t1")
    pt2 = PlaylistTrack(playlist_id='pl1', track_id="t2")
    pt3 = PlaylistTrack(playlist_id='pl1', track_id="t3")

    pt4 = PlaylistTrack(playlist_id='pl2', track_id="t4")
    pt5 = PlaylistTrack(playlist_id='pl2', track_id="t5")

    db.session.add_all([pt1, pt2, pt3, pt4, pt5])
    db.session.commit()


def connect_to_db(app, database="postgresql:///spotify"):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Running this module interactively will leave you in a
    # state of being able to work with the db directly

    from server import app
    connect_to_db(app)
    print("Connected to DB.")