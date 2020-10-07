import spotipy
from spotipy.oauth2 import SpotifyOAuth


def spotify_client():
    scope = "user-library-read playlist-modify-private playlist-modify-public"

    client_id = 'e904f73835b24d0ab4e8c2ec0194ec25'
    client_secret = '1122b4835ab6422890c30e49407076a1'
    redirect_uri = 'https://www.google.es/'
    username = 'dtd9srb32n2qbzn2c35j4iutg'
    auth_manager = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,username=username,scope=scope)

    return spotipy.Spotify(auth_manager=auth_manager)

sp = spotify_client()


results = sp.current_user_saved_tracks()

pl = sp.current_user_playlists()

plid = [x["id"] for x in pl['items']]   # user playlists id

for pid in plid:
    sp.current_user_unfollow_playlist(pid)

print('yeah')