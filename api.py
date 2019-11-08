import spotipy, sys, os
import spotipy.util as util

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

class Spotify:

    def get_access_token(self):
        """Return access token from Spotify for defined scopes."""

        scope = 'user-library-read'

        # Get access token from Spotify authorization server.
        token = util.prompt_for_user_token(self.username, scope, 
                                        client_id = SPOTIPY_CLIENT_ID, 
                                        client_secret = SPOTIPY_CLIENT_SECRET, 
                                        redirect_uri = SPOTIPY_REDIRECT_URI)

        if token:
            return token 
        else:
            return None


    def __init__(self, username):
        """Get Spotify oAuth authroization and store attributes."""

        self.username = username
        self.token = self.get_access_token()
        self.sp = spotipy.Spotify(auth=self.token)


    def get_playlist_tracks(playlist_list=['5vt2cOxZrcn9yVzTTIURJe', '4xP6FbKJ28lbo9JSqJ9MbZ']):
        """Print all the tracks in a playlist."""

        compiled_playlist_tracks = {}

        for playlist_id in playlist_list:

            # Get all tracks of a playlist.
            results = self.sp.user_playlist_tracks(self.username, playlist_id)
            playlist_tracks = results['items']

            # If number of tracks exceeds the limit,
            # continue getting the next set until all tracks are retrieved.
            while results['next']:
                results = self.sp.next(results)
                playlist_tracks.extend(results['items'])
            
            # Add to dictionary where key = playlist_id and value = list of tracks
            for item in playlist_tracks:
                track = item['track']
                playlist = compiled_playlist_tracks.get(playlist_id, [])
                playlist.append(track['id'])
        print(compiled_playlist_tracks)
        return compiled_playlist_tracks


    def get_playlists():
        """Print all user playlists."""

        # Get user playlists
        results = self.sp.user_playlists(username)
        playlists = results['items']

        # Number of playlists retrieved in inital call is limited.
        # If the user has more playlists than the limit, retrieve the remaining.
        while results['next']:
            results = self.sp.next(results)
            playlists.extend(results['items'])
        
        print(playlists)
        return playlists


    def get_track_audio_features(track_list=['0Brf1s65f8eekORKK9gpe4', '3hYdai5p5sQ3vAmHQ6uaK6']):
        """Print audio features of a track."""

        # Audio_features function returns a list of dictionaries.
        track_fts = self.sp.audio_features(track_list)
        print(track_fts)
        return track_fts

        # for track in track_fts:
        #     #General info of track
        #     track_id = track['id']
        #     track_general_info = self.sp.track(track_id)
        #     name = track_general_info['name']
        #     # artist = 
        #     user_id = self.username
        #     # playlist_id = 

        #     # Track features
        #     key = track['key']
        #     mode = track['mode']
        #     danceability = track['danceability']
        #     energy = track['energy']
        #     instrumentalness = track['instrumentalness']
        #     loudness = track['loudness']
        #     speechiness = track['speechiness']
        #     valence = track['valence']   
        #     tempo = track['tempo']   
        #     uri = track['uri']   
        #     href = track['track_href']   
        #     duration = track['duration_ms'] 
        #     print(f"key: {key}, mode: {mode}, energy: {energy}, tempo: {tempo}, uri: {uri}")   
