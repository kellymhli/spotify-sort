import spotipy, sys, os
import spotipy.util as util

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

def get_access_token(username):
    """Return access token from Spotify for defined scopes."""

    scope = 'user-library-read'

    # Get access token from Spotify authorization server
    token = util.prompt_for_user_token(username, scope, 
                                       client_id = SPOTIPY_CLIENT_ID, 
                                       client_secret = SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri = SPOTIPY_REDIRECT_URI)

    if token:
        return token 
    else:
        return None


def authorize(username):
    """Instantiate Spotify object for user using given username."""

    token = get_access_token(username)
    sp = spotipy.Spotify(auth=token)
    
    get_playlists(username, sp)


def get_playlist_tracks(username, playlist_id, sp):
    """Return all the tracks in a playlist."""

    playlist_tracks = sp.user_playlist_tracks(username, playlist_id)
    for item in playlist_tracks:
        track = item['track']
        print(f"{track['name']} - {track['artists'][0]['name']}")
        
    # results = sp.current_user_saved_tracks(limit=50)
    # for item in results['items']:
    #     track = item['track']
    #     print(f"{track['name']} - {track['artists'][0]['name']}")


def get_playlists(username, sp):
    """Return a list of all user playlists."""

    results = sp.user_playlists(username)
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])

    for playlist in playlists:
        if playlist['owner']['id'] == username:
            print(f"{playlist['id']}|||{playlist['name']}|||{playlist['owner']['id']}")



