from FlaskWebProject1.sqlutils import insertMany, insertOne, checkProduct
import pickle


# save song in sql
def saveSongs(x,v):
    saveRes(x,v)
    addSongs(x,v)
    a = 2



def addSongs(x,v):

    addVideo(v)
    addArtists(x)
    addAlbums(x)
    addTracks(x)
    addRelations(x,v)
    

## SONGS
def addArtists(res):
    table = 'artist'
    arr = [x['artist_db'] for x in res]
    values = [ x for X in arr for x in X]

    addProduct(values,3,1)
    insertMany(table,values)

def addAlbums(res):
    # label
    table = 'label'
    label_name = [x['label'] for x in res]
    [all_label,new_label] = checkProduct(table,label_name)

    addProduct(new_label,5,1)
    insertMany(table,new_label)

    # add label_id to songs
    for d, l in zip(res, all_label):
        d.update({'label_id':l[0]})

    # album
    table = 'album'
    values = [(x['album_id'],x['album'],x['atype'],x['label_id'],x['himg']) for x in res]
    addProduct(values,2,1)
    insertMany(table,values)

    # album 2 artist
    table = 'album2artist'
    arr = [x['artist_db']+[x['album_id']] for x in res]
    values = []
    for x in arr:
        album_id = x[-1]
        for i in range(len(x)-1):
            values.append((album_id,x[i][0]))
    insertMany(table,values)            
            

def addTracks(res):
    # tracks
    table = 'track'
    values = [(x['id'],x['name'],x['album_id'],x['artist'],x['href'],x['hmp3'],x['dur'],x['bpm'],x['pop']) for x in res]
    addProduct(values,1,1)
    insertMany(table,values)

    # track 2 artists
    table = 'track2artist'
    values = []
    for x in res:
        track_id = x['id']
        artist = x['artist_db']
        for a in artist:
            artist_id = a[0]
            values.append((track_id,artist_id))   
    insertMany(table,values)

## VIDEO 
def addVideo(v):

    # foreign
    addChannel(v)
    addPlaylist(v)
    # video
    table = 'video'
    v_id = v['id']
    name = v['name']
    ch_id = v['channel']['id']
    artist_id = 0
    views = v['views']
    likes = v['likes']
    comments = v['comments']
    hspt = v['hspt']
    himg = v['himg']
    nsongs = v['nsongs']
    values = (v_id,name,ch_id,artist_id,views,likes,comments,hspt,himg,nsongs)
    addProduct(values,8,0)
    insertOne(table,values)


def addChannel(v):
    table = 'channel'
    ch_id = v['channel']['id']
    name = v['channel']['name']
    values = (ch_id,name)
    addProduct(values,9,0)
    insertOne(table,values)

def addPlaylist(v):
    table = 'playlist'
    pl_id = v['hspt']
    name = v['name']
    user_id = 'dtd9srb32n2qbzn2c35j4iutg'
    values = (pl_id,name,user_id)
    addProduct(values,4,0)
    insertOne(table,values)

## RELATIONS
def addRelations(res,v):
    tables = ['track2video','track2playlist']
    cols = ['id','hspt']

    for i in range(len(tables)):

        table = tables[i]
        col = cols[i]
        values = []

        for idx,x in enumerate(res):
            track_id = x['id']
            values.append((track_id,v[col],idx+1))   
            
        insertMany(table,values)






## PRODUCT
def addProduct(values,ptype,m):
    if m==0:
        insertOne('product',(values[0],values[1],ptype))
    else:
        vals = [(x[0],x[1],ptype) for x in values]
        insertMany('product',vals)



# temp variables
def saveRes(x,v):
    with open('songs.pickle', 'wb') as f:
        pickle.dump([x,v],f)

def openRes():
    with open('songs.pickle', 'rb') as f:
        [x,v] = pickle.load(f)
    return [x,v]




   