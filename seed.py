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


def load_keys():
    """Load music keys into database."""

    Key.query.delete()
    
    for row in open("seed_data/u.keys"):
        row = row.rstrip()
        row_list = row.split("|")

        # Parse file to get key id and name
        key_id = row_list[0]
        key_name = row_list[1:]  # List as some keys have more than one name
        print(key_id, key_name)

        # Create new key entry for database.
        key = Key(key_id = key_id,
                  key_name = key_name)    

        db.session.add(key)

    db.session.commit()    


def load_matching_keys():
    """Load keys' matching keys into database."""

    MatchingKey.query.delete()

    for row in open("seed_data/u.keymatch"):
        row = row.rstrip()
        pair, key, match = row.split("|")

        matching_key = MatchingKey(key_pair = pair,
                                   key_id = key,
                                   matching_key = match)
        
        db.session.add(matching_key)
    
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import data into db
    load_playlists()
    load_keys()
    load_matching_keys()