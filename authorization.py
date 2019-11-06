import spotipy, sys, os
import spotipy.util as util

SPOTIPY_CLIENT_ID = (os.environ.get('SPOTIPY_CLIENT_ID'))
SPOTIPY_CLIENT_SECRET = (os.environ.get('SPOTIPY_CLIENT_SECRET'))
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

print(f"{SPOTIPY_CLIENT_ID}")
print(f"{SPOTIPY_CLIENT_SECRET}")

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print(f"Usage: {username}")
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(f"{track['name']} - {track['artists'][0]['name']}")
else:
    print(f"Can't get token for {username}")
