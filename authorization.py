import spotipy, sys, os
import spotipy.util as util

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

def authorize(username):
    """Take in username and prompt user to authorize access to Spotify data."""

    scope = 'user-library-read'

    # Get access token from Spotify authorization server
    token = util.prompt_for_user_token(username, scope, 
                                       client_id = SPOTIPY_CLIENT_ID, 
                                       client_secret = SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri = SPOTIPY_REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(f"{track['name']} - {track['artists'][0]['name']}")
    else:
        print(f"Can't get token for {username}")