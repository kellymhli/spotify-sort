# Functions that take in json objects returned from api.py
# and seeds spotify database with that data

import api, random, string
from model import User, Playlist, PlaylistTrack, Track, Key, MatchingKey, connect_to_db, db

def load_playlists(spotify_id, token):
    """Load playlists into database."""

    playlists = api.get_playlists(spotify_id, token)

    for playlist in playlists:

        # Check if playlist already in db
        if Playlist.query.filter(Playlist.playlist_id == playlist['id']).one_or_none() == None:

            # Create new playlist row
            playlist = Playlist(playlist_id = playlist['id'],
                                pl_name = playlist['name'],
                                spotify_id = playlist['owner']['id'])

            # Add playlist to database
            db.session.add(playlist)

    # Commit added playlists to database.
    db.session.commit()


def add_playlist(spotify_id, pl_name, track_ids):
    """Add user generated playlist into database."""

    # Spotify playlist_id's are 22 char long, make custom id's 30 long
    playlist_id = ''.join([random.choice(string.ascii_letters + string.digits)
                      for n in range(30)])

    # Create new playlist and add to db
    if Playlist.query.filter(Playlist.playlist_id == playlist_id).one_or_none() == None:
        playlist = Playlist(playlist_id=playlist_id,
                            pl_name=pl_name,
                            spotify_id=spotify_id)

        db.session.add(playlist)

        # Add track and playlist ids to playlist_tracks table
        for track_id in track_ids:
            playlist_track = PlaylistTrack(playlist_id = playlist_id,
                                           track_id = track_id)
            db.session.add(playlist_track)

    db.session.commit()


def load_tracks(spotify_id, token, tracks, playlist_id):
    """Load track into database."""

    print(f'Loading tracks from playlist: {playlist_id}')

    # Get detailed audio features of each track in a list of tracks
    tracks_feats = api.get_track_audio_features(token, tracks)

    for track in tracks_feats:
        # Different call to general info of a track given the id
        track_general_info = api.get_track_general_info(token, track['id'])

        # Only add track to db if one instance of it is not there already
        if Track.query.filter(Track.track_id == track['id']).one_or_none() == None:
            add_track = Track(track_id = track['id'],
                              track_name = track_general_info['name'],
                              artist = track_general_info['album']['artists'][0]['name'],
                              spotify_id = spotify_id,
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


def load_playlist_tracks(spotify_id, token):
    """Load tracks from a list of playlists into database."""

    PlaylistTrack.query.delete()

    # Get a list of a user's playlists
    playlists = db.session.query(Playlist.playlist_id)
    user_playlists = playlists.filter(Playlist.spotify_id == spotify_id).all()
    playlist_list = [playlist[0] for playlist in user_playlists]

    # Get tracks from user's playlists
    playlist_tracks = api.get_playlist_tracks(spotify_id, token, playlist_list = playlist_list)

    for playlist_id, tracks in playlist_tracks.items():

        num_tracks = len(tracks)
        print(num_tracks)
        start_list = 0
        end_list = 50

        # Spotipy API call is limited to 50 tracks per call
        # Make multiple calls to load tracks of playlists with >50 tracks
        while num_tracks > 50:
            print(start_list, end_list, num_tracks)
            tracks_list = tracks[start_list : end_list]
            # Load tracks from playlist into tracks table in db
            load_tracks(spotify_id, token, tracks_list, playlist_id)
            start_list += 50
            end_list += 50
            num_tracks -= 50
            print(num_tracks)

        tracks_list = tracks[start_list : start_list + num_tracks]
        load_tracks(spotify_id, token, tracks_list, playlist_id)

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


def load_user(user_id, spotify_id, password, token):
    """Load user information into database."""

    # Update user token in db if user already in the db
    # Otherwise create new user and add to db
    user_info = User.query.get(user_id)
    if user_info != None:
        user_info.token = token
    else:
        user = User(user_id = user_id,
                    spotify_id = spotify_id,
                    password = password,
                    token = token)
        db.session.add(user)

        # Load user's playlists, and tracks into db upon creating new user
        load_playlists(spotify_id, token)
        print("load playlists")
        load_playlist_tracks(spotify_id, token)
        print("load playlist tracks")

    db.session.commit()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    # Incase tables haven't been created, create them
    db.create_all()
    load_keys()
    load_matching_keys()