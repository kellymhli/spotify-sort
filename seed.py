# Functions that take in json objects returned from api.py 
# and seeds spotify database with that data

import api
from model import User, Playlist, PlaylistTrack, Track, Key, MatchingKey, connect_to_db, db
from server import app

def load_user():
    """Load user information into database."""

    pass


def load_playlists():
    """Load playlists into database."""
    
    Playlist.query.delete()
    playlists = api.get_playlists()  #pass in username and sp

    for playlist in playlists[1:]:

        # Create new playlist row
        playlist = Playlist(playlist_id = playlist['id'],
                            pl_name = playlist['name'],
                            user_id = playlist['owner']['id'])
        
        # Add playlist to database
        db.session.add(playlist)
    
    # Commit added playlists to database.
    db.session.commit()


def load_playlist_tracks():
    """Load tracks from a list of playlists into database."""

    TrackPlaylist.query.delete()
    playlist_tracks = api.get_playlist_tracks()  #pass in username, sp, and list of playlists

    for playlist_id, tracks in playlist_tracks:
        for track in tracks:
            playlist_track = PlaylistTrack(playlist_id = playlist_id,
                                           track_id = track['id'])
        
        db.session.add(playlist_track)
    
    db.session.commit()


def load_tracks():
     
     Track.query.delete()
     tracks = api.get_track_audio_features()  # pass in username, sp, and list of tracks

     for track in tracks:
         add_track = Track(track_is = track['id'],
                           key = track['key'],
                           mode = track['mode'],
                           danceability = track['danceability'],
                           energy = track['energy'],
                           instrumentalness = track['instrumentalness'],
                           loudness = track['loudness'],
                           speechiness = track['speechiness'],
                           valence = track['valence'],
                           tempo = track['tempo'],
                           uri = track['uri'],
                           href = track['track_href'],
                           duration = track['duration_ms'])
                           # name, user_id, playlist_id

        db.session.add(add_track)
    
    db.session.commit()


def load_keys():
    """Load music keys into database."""
    
    for row in open("seed_data/u.keys"):
        row = row.rstrip()
        row_list = row.split("|")

        # Parse file to get key id and name
        key_id = row_list[0]
        key_name = row_list[1:]  # List as some keys have more than one name

        # Create new key entry for database.
        key = Key(key_id = key_id,
                  key_name = key_name)    

        db.session.add(key)

    db.session.commit()   
    print("Loaded keys to db.") 


def load_matching_keys():
    """Load keys' matching keys into database."""

    for row in open("seed_data/u.keymatch"):
        row = row.rstrip()
        pair, key, match = row.split("|")

        matching_key = MatchingKey(key_pair = pair,
                                   key_id = key,
                                   matching_key = match)
        
        db.session.add(matching_key)
    
    db.session.commit()
    print("Loaded matching keys to db.")


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import data into db
    load_keys()
    load_matching_keys()
    load_playlists()
    load_playlist_tracks()
    load_tracks()