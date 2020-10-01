import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from itertools import compress

def spotify_client():
    client_id = '5a170e03cdce4c0ba9a68a1619a0bf8a'
    client_secret = '0fcc2a96ee4a4709b7f911902ccbf079'
    auth_manager = SpotifyClientCredentials(client_id,client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

# search songs in youtube and get the spotify link
def find_songs(songs_list):
    songs_format = list(filter(None,list(map(checkline,songs_list))))   # remove index, labels and useless information
    songs_found = list(map(getSpotifyName,songs_format))    # songs found in spotify
    bool_list = list(map(lambda x,y:checkSong(x,y), songs_format, songs_found)) # check that song found is the same as the youtube
    songs_checked = list(compress(songs_found, bool_list)) # list of songs

    return songs_checked

def textarea2list(video):
    # clean songs input
    songs = video["comments"] 
    songs = songs.replace('\r','')
    songs = songs.split('\n')
    return list(dict.fromkeys(songs))


def checkline(x):
    
       
        try:
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
            if song == 'id id' or '????' in song:
                song = ''
        except:
            song = ''

        return song

def getSpotifyName(x):

    # search song in spotify
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
        return song
    else:
        return ''

def checkSong(s1,s2):
    if s1 and s2:
        track = s2[1].lower()
        artist = s2[2].lower()
        album = s2[3].lower()
        checker = track + ' ' + artist + ' ' + album
        if all(x in checker for x in s1.split()):
            return True
        else:
            return False
    else:
        return False


# print functions
def getArtistString(artists):
    sartist = ''
    for x in artists:
        sartist += x['name'] + ' & '
    sartist = sartist[:-3]
    return sartist

def print2songs(idx,songs_found,songs_format):
    track = songs_found[idx][1].lower()
    artist = songs_found[idx][2].lower()
    checker = track + ' ' + artist
    print(checker)
    print(songs_format[idx])

sp = spotify_client()