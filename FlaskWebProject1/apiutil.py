from FlaskWebProject1.sputils import textarea2list, find_songs, createPlaylist
from FlaskWebProject1.ytutils import getVideo, getVideoID
from FlaskWebProject1.songutils import saveSongs, openRes
from FlaskWebProject1.sqlutils import checkVideo
from FlaskWebProject1.ytscrap import getSongs


def link2data(url):
    vid = getVideoID(url)
    [b,songs,v] = checkVideo(vid)
    if b == 0:
        v =  getVideo(url)                                  # dict video with info
        songs_list1 = textarea2list(v['comments'])          # get tracklist from comments of video
        songs_list2 = getSongs(url)                         # get songs from "music in this video"
        songs = find_songs(songs_list1,songs_list2)          # songs found in spotify
        v['hspt'] = createPlaylist(songs,v['name'])         # add sp link to video 
        v['nsongs'] = len(songs)                            # n songs found
        saveSongs(songs,v)                                  # add songs to sql database
    return [songs,v]

    
