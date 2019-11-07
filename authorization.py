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

token = get_access_token(username)
sp = spotify.Spotify(auth=token)
