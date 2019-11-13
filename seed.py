# Functions that take in json objects returned from api.py 
# and seeds spotify database with that data

import api
from model import User, Playlist, PlaylistTrack, Track, Key, MatchingKey, connect_to_db, db

def load_user(username, token):
    """Load user information into database."""

    # Update user token in db if user already in the db
    # Otherwise create new user and add to db
    user_info = User.query.get(username)
    if user_info != None:
        user_info.token = token
    else:
        user = User(user_id = username, 
                    token = token)
        db.session.add(user)

    db.session.commit()


def load_playlists(user_id, token):
    """Load playlists into database."""

    Playlist.query.delete()

    playlists = api.get_playlists(user_id, token)  # Get a list of all 

    for playlist in playlists:
        # Create new playlist row
        playlist = Playlist(playlist_id = playlist['id'],
                            pl_name = playlist['name'],
                            user_id = playlist['owner']['id'])
        
        # Add playlist to database
        db.session.add(playlist)
    
    # Commit added playlists to database.
    db.session.commit()


def load_tracks(user_id, token, tracks, playlist_id):
    """Load track into database."""

    print(f'Loading tracks from playlist: {playlist_id}')
    
    # Get detailed audio features of each track in a list of tracks
    tracks_feats = api.get_track_audio_features(token, tracks)

    for track in tracks_feats:
        # Different call to general info of a track given the id
        track_general_info = api.get_track_general_info(token, track['id'])

        if Track.query.filter(Track.track_id == track['id']).one_or_none() == None:
            add_track = Track(track_id = track['id'],
                              user_id = user_id, 
                              playlist_id = playlist_id, 
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
                              duration = track['duration_ms']
                              )
            db.session.add(add_track)
    
    db.session.commit()


def load_playlist_tracks(user_id, token):
    """Load tracks from a list of playlists into database."""

    PlaylistTrack.query.delete()

    # Get a list of a user's playlists
    playlists = db.session.query(Playlist.playlist_id)
    user_playlists = playlists.filter(Playlist.user_id == user_id).all()
    playlist_list = [playlist[0] for playlist in user_playlists]

    # Get tracks from user's playlists
    playlist_tracks = api.get_playlist_tracks(user_id, token, playlist_list = playlist_list)

    for playlist_id, tracks in playlist_tracks.items():
        # Load tracks from playlist into tracks table in db
        load_tracks(user_id, token, tracks, playlist_id)

        # Add track and playlist ids to playlist_tracks table
        for track in tracks:
            playlist_track = PlaylistTrack(playlist_id = playlist_id,
                                           track_id = track)
            db.session.add(playlist_track)
    
    db.session.commit()


def load_keys():
    """Load music keys into database."""
    
    # Delete and tables everytime seed.py is called to prevent multiple entries
    MatchingKey.query.delete()
    Key.query.delete()

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

    from server import app
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    users = db.session.query(User.user_id, User.token).all()  # Get users from db

    load_keys()
    load_matching_keys()

    # Import info into db
    for user_id, token in users:
        load_playlists(user_id, token)
        load_playlist_tracks(user_id, token)