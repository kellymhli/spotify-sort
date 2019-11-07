# Functions that take in json objects returned from api.py 
# and seeds spotify database with that data

import api
from model import User, Playlist, TrackPlaylist, Track, Key, MatchingKey
from server import app

def load_user():
    """Load user information into database."""

    pass


def load_playlists(playlists):
    """Load playlists into database."""
    # playlists = [username, [playlist_id, pl_name], [playlist_id, pl_name]]
    
    uaer_id = playlist[0]  # username

    for playlist_id, pl_name in playlists[1:]:

        # Create new playlist row
        playlist = Playlist(playlist_id = playlist_id,
                            pl_name = pl_name,
                            user_id = user_id)
        
        # Add playlist to database
        db.session.add(playlist)
    
    # Commit added playlists to database.
    db.session.commit()
