import spotipy, sys, os
import spotipy.util as util

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

def get_access_token(username):
    """Return access token from Spotify for defined scopes."""

    scope = 'user-library-read'

    # Get access token from Spotify authorization server.
    token = util.prompt_for_user_token(username, scope, 
                                       client_id = SPOTIPY_CLIENT_ID, 
                                       client_secret = SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri = SPOTIPY_REDIRECT_URI)

    if token:
        return token 
    else:
        return None


def get_playlist_tracks(username, sp, playlist_list=['5vt2cOxZrcn9yVzTTIURJe', '4xP6FbKJ28lbo9JSqJ9MbZ']):
    """Print all the tracks in a playlist."""

    file = open('seed_data/u.playlist-tracks', 'w+')
    for playlist_id in playlist_list:

        # Get all tracks of a playlist.
        results = sp.user_playlist_tracks(username, playlist_id)
        playlist_tracks = results['items']

        # If number of tracks exceeds the limit,
        # continue getting the next set until all tracks are retrieved.
        while results['next']:
            results = sp.next(results)
            playlist_tracks.extend(results['items'])

        for item in playlist_tracks:
            track = item['track']
            file.write(f"{playlist_id}|||{track['id']}\n")

    file.close()
    
    # Tracks of user's saved songs list (songs not in a playlist) 
    # results = sp.current_user_saved_tracks()
    # playlist_tracks = results['items']
    # while results['next']:
        # results = sp.next(results)
        # playlist_tracks.extend(results['items'])


def get_playlists(username, sp):
    """Print all user playlists."""

    # Get user playlists
    results = sp.user_playlists(username)
    playlists = results['items']

    # Number of playlists retrieved in inital call is limited.
    # If the user has more playlists than the limit, retrieve the remaining.
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])

    # Open file in seed_data directory to write playlist data into.
    file = open('seed_data/u.playlists', 'w+')

    # Print playlist_id, playlist_name, and username to file.
    for playlist in playlists:
        if playlist['owner']['id'] == username:
            file.write(f"{playlist['id']}|||{playlist['name']}|||{playlist['owner']['id']}\n")

    file.close()


def get_track_audio_features(username, sp, track_list=['0Brf1s65f8eekORKK9gpe4']):
    """Print audio features of a track."""

    # Audio_features funtion returns a list of dictionaries.
    track_fts = sp.audio_features(track_list)
    for track in track_fts:
        #General info of track
        track_id = track['id']
        track_general_info = sp.track(track_id)
        name = track_general_info['name']
        # artist
        user_id = username
        # playlist_id

        # Track features
        key = track['key']
        mode = track['mode']
        danceability = track['danceability']
        energy = track['energy']
        instrumentalness = track['instrumentalness']
        loudness = track['loudness']
        speechiness = track['speechiness']
        valence = track['valence']   
        tempo = track['tempo']   
        uri = track['uri']   
        href = track['track_href']   
        duration = track['duration_ms'] 
        print(f"key: {key}, mode: {mode}, energy: {energy}, tempo: {tempo}, uri: {uri}")   


def authorize(username):
    """Instantiate Spotify object for user using given username."""

    token = get_access_token(username)
    sp = spotipy.Spotify(auth=token)
    
    get_playlists(username, sp)
    get_playlist_tracks(username, sp)
    get_track_audio_features(username, sp)
