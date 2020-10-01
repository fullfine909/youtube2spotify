from flask import Flask, redirect, url_for, render_template, request
from sputils import textarea2list, find_songs
from ytutils import getVideo, getVideoID
from songutils import saveSongs

url = 'https://www.youtube.com/watch?v=W91KoUTQnmw&t=2708s&ab_channel=H%C3%96RBERLIN'
video =  getVideo(url)                  # dict video with info
songs_list = textarea2list(video)       # get tracklist from comments of video
songs = find_songs(songs_list)          # songs found in spotify
saveSongs(songs,video)                  # add songs to sql database