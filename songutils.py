from sqlutils import insertMany, insertOne
import pickle



# save song in sql
def saveSongs(x,yt):
    #saveRes(x,yt)
    #addSongs(x,yt)
    print('you')






def addSongs(x,yt):

    addArtists(x)
    addAlbums(x)
    addTracks(x)
    addVideo(yt)




def addArtists(res):
    spvalue = 'artists'
    table = 'artist'
    arr = [x[spvalue] for x in res]
    values = [(x['id'],x['name']) for sub in arr for x in sub ]
    names = 'id, name'
    insertMany(table,names,values)

def addAlbums(res):
    spvalue = 'album'
    table = 'album'
    arr = [x[spvalue] for x in res]
    values = [(x['id'],x['name']) for x in arr]
    names = 'id, name'
    insertMany(table,names,values)

def addTracks(res):
    table = 'track'
    values = [(x['id'],x['name']) for x in res]
    names = 'id, name'
    insertMany(table,names,values)

def addVideo(v):
    table = 'video'
    att = 2
    values = (v["id"],v["title"],v["views"],v["likes"],v["comments"])


def tracks2youtube(res,yt):
    print('yeah')


# temp variables
def saveRes(res,yt):
    with open('train.pickle', 'wb') as f:
        pickle.dump([res,yt],f)

def openRes():
    with open('train.pickle', 'rb') as f:
        [res,yt] = pickle.load(f)
    return [res,yt]




   