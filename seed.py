# Functions that take in json objects returned from api.py 
# and seeds spotify database with that data

import api
from model import User, Playlist, TrackPlaylist, Track, Key, MatchingKey, connect_to_db, db
from server import app

def load_user():
    """Load user information into database."""

    pass


def load_playlists():
    """Load playlists into database."""
    
    Playlist.query.delete()
    playlists = api.get_playlists()

    for playlist in playlists[1:]:

        # Create new playlist row
        playlist = Playlist(playlist_id = playlist['id'],
                            pl_name = playlist['name'],
                            user_id = playlist['owner']['id'])
        
        # Add playlist to database
        db.session.add(playlist)
    
    # Commit added playlists to database.
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import data into db
    load_playlist()