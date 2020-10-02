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
    songs_found = list(map(getSpotifySong,songs_format))                # songs found in spotify
    bool_list = list(map(lambda x,y:checkSong(x,y), songs_format, songs_found)) # check that song found is the same as the youtube
    songs_checked = list(compress(songs_found, bool_list)) # list of songs
    song_metadata = addData(songs_checked)

    return song_metadata

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
            to_replace = [':','-','&','?','feat','. ','unreleased','original mix','(',') ',')','"']
            for r in to_replace:
                x = x.replace(r, '')

            # delte
            to_delete = ['????','tracklist']
            if any(d in x for d in to_delete):
                x = ''

            # delete collection
            p = x.rfind('[')
            if p > 0:
                x = x[:p-1]

            # delete time / index
            x = x.split()
            x.pop(0)

            # join words into a string
            x = ' '.join(x)

            # nina
            if x[0:2] == 'id' and x[-2:] == 'id':
                x = ''

            
        except:
            x = ''

        return x

def getSpotifySong(x):

    # search song in spotify
    result = sp.search(x,type='track',limit=1)
    if (len(result['tracks']['items']) > 0):
        track = result['tracks']['items'][0]

        song = {
            'id':track['id'],
            'name':track['name'],
            'artist':getArtistString(track['artists']),
            'album':track['album']['name'],
            'album_id':track['album']['id'],
            'href':track['external_urls']['spotify'],
            'hmp3':track['preview_url'],
            'image':track['album']['images'][2]['url'],
            'pop':track['popularity']}

        return song
    else:
        return ''

def checkSong(s1,s2):
    if s1 and s2:
        track = s2["name"].lower()
        artist = s2["artist"].lower()
        album = s2["album"].lower()
        checker = track + ' ' + artist + ' ' + album
        if all(x in checker for x in s1.split()):
            return True
        else:
            return False
    else:
        return False

def addData(songs):
    # track objects
    if songs != []:
        t = [x['id'] for x in songs]
        resT = sp.audio_features(t)

        # album objects
        a = [x['album_id'] for x in songs]
        resA = sp.albums(a)

        for i in range(len(songs)):
            songs[i].update({'bpm':round(resT[i]['tempo'])})
            songs[i].update({'label':resA['albums'][i]['label']})

    return songs


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