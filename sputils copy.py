import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def spotify_client():
    client_id = '5a170e03cdce4c0ba9a68a1619a0bf8a'
    client_secret = '0fcc2a96ee4a4709b7f911902ccbf079'
    auth_manager = SpotifyClientCredentials(client_id,client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


def checkline(x):
    
        # lower
        x = x.lower()

        # replace characters
        to_replace = [':','-','&','?','feat','. ','unreleased','original mix','(',')']
        for r in to_replace:
            x = x.replace(r, '')

        # delete collection
        p = x.rfind('[')
        if p > 0:
            x = x[:p-1]

        # delete time / index
        x = x.split()
        x.pop(0)

        # join words into a string
        song = ' '.join(x)

        # delte id - id
        if song == 'id id':
            song = ''

        return song

def getArtistString(artists):
    sartist = ''
    for x in artists:
        sartist += x['name'] + ' & '
    sartist = sartist[:-3]
    return sartist


def getSpotifyNames(songs_input):

    # spotif client
    sp = spotify_client()

    # clean songs input
    songs_input = songs_input.replace('\r','')
    songs_input = songs_input.split('\n')

    songs = []
    for x in songs_input:
        songs.append(checkline(x))

    songs = list(filter(None, songs))


    # search songs in spotify
    songsfound = []
    songsmissed = []
    for x in songs:
        result = sp.search(x,type='track',limit=1)
        if (len(result['tracks']['items']) > 0):
            track = result['tracks']['items'][0]
            track_id = track['id']
            name = track['name']
            artist = getArtistString(track['artists'])
            album = track['album']['name']
            albumid = track['album']['id']
            href = track['external_urls']['spotify']
            image = track['album']['images'][2]['url']
            pop = track['popularity']
            album_result = sp.album(album_id=albumid)
            label = album_result['label']
            song = [track_id,name,artist,album,href,image,pop,label]
            songsfound.append(song)
        else:
            songsmissed.append(x)

    return songsfound