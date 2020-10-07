import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from itertools import compress
from FlaskWebProject1.myutils import divide_chunks, similarity


def spotify_client():
    client_id = 'e904f73835b24d0ab4e8c2ec0194ec25'
    client_secret = '1122b4835ab6422890c30e49407076a1'
    auth_manager = SpotifyClientCredentials(client_id,client_secret)

    return spotipy.Spotify(auth_manager=auth_manager)

def spotify_clientOA():
    scope = "user-library-read playlist-modify-private playlist-modify-public"

    client_id = 'e904f73835b24d0ab4e8c2ec0194ec25'
    client_secret = '1122b4835ab6422890c30e49407076a1'
    redirect_uri = 'http://ys5-env.eba-mjmi37yf.eu-west-1.elasticbeanstalk.com/23444/'
    username = 'dtd9srb32n2qbzn2c35j4iutg'
    auth_manager = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,username=username,scope=scope)

    return spotipy.Spotify(oauth_manager=auth_manager)

# search songs in youtube and get the spotify link
def find_songs(songs_list):
    songs_format = list(filter(None,list(map(checkline,songs_list))))   # remove index, labels and useless information
    songs_unique = uniqueSearch(songs_format)                           # delete duplicate songs (two comments) for sp search
    songs_found = list(map(getSpotifySong,songs_unique))                # songs found in spotify
    bool_list = list(map(lambda x,y:checkSong(x,y), songs_format, songs_found)) # check that song found is the same as the youtube
    songs_checked = list(compress(songs_found, bool_list)) # list of songs
    song_metadata = addData(songs_checked)

    return song_metadata

def textarea2list(comments):
    # clean songs input
    songs = comments.replace('\r','')
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

def uniqueSearch(x):
    return list(dict.fromkeys(x))

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
        sim = similarity(s1,checker)
        return sim
    else:
        return False

def addData(songs):
    # track objects
    if songs != []:
        # tracks
        t = [x['id'] for x in songs]
        resT = chunkApi(t,50,sp.audio_features)
        resTm = [j for i in resT for j in i]  # merge sublists

        # album objects
        a = [x['album_id'] for x in songs]
        resA = chunkApi(a,20,sp.albums)
        resAm = [j for i in resA for j in i['albums']] # merge sublists

        for i in range(len(songs)):
            songs[i].update({'bpm':round(resTm[i]['tempo'])})
            songs[i].update({'label':resAm[i]['label']})

    return songs

# playlist
def createPlaylist(x,name):
    #deletePlaylists()

    user = 'dtd9srb32n2qbzn2c35j4iutg'

    cu_pl = spOA.current_user_playlists()
    names = [p['name'] for p in cu_pl['items']]

    if name not in names:

        playlist = spOA.user_playlist_create(user=user,name=name)
        playlist_id = playlist["id"]
        items = [t['id'] for t in x]
        spOA.playlist_add_items(playlist_id=playlist_id,items=items)

        return playlist_id

    else:

        return cu_pl['items'][0]['id']

def deletePlaylists():
    playlists = spOA.current_user_playlists()
    ids = [x['id'] for x in playlists['items']]
    for x in ids:
        spOA.current_user_unfollow_playlist(x)

# chunk api
def chunkApi(x,n,b):
    xc = list(divide_chunks(x,n))   # divide x in chunks
    res = []
    for c in xc:
        res.append(b(c))

    return res

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
spOA = spotify_clientOA()
