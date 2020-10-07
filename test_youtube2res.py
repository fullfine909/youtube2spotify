from flask import Flask, redirect, url_for, render_template, request
from sputils import textarea2list, find_songs, createPlaylist
from ytutils import getVideo, getVideoID
from songutils import saveSongs, openRes

url = 'https://www.youtube.com/watch?v=4utKO75DtBE&t=297s&ab_channel=BE-AT.TV'
v =  getVideo(url)                                  # dict video with info
songs_list = textarea2list(v['comments'])           # get tracklist from comments of video
songs = find_songs(songs_list)                      # songs found in spotify
v["sp_url"] = createPlaylist(songs,v['title'])      # add sp link to video    
saveSongs(songs,v)                                  # add songs to sql database

