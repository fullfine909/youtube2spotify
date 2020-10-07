from flask import render_template, request
from FlaskWebProject1 import app
from FlaskWebProject1.sputils import textarea2list, find_songs, createPlaylist
from FlaskWebProject1.ytutils import getVideo, getVideoID
from FlaskWebProject1.songutils import saveSongs, openRes


@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        url = request.form["link_input"]                    # yt url
        v =  getVideo(url)                                  # dict video with info
        songs_list = textarea2list(v['comments'])           # get tracklist from comments of video
        songs = find_songs(songs_list)                      # songs found in spotify
        v["sp_url"] = createPlaylist(songs,v['title'])      # add sp link to video 
        saveSongs(songs,v)                                  # add songs to sql database
        # [songs,yt] = openRes()
        return render_template("index2.html",arr=songs,video=v)
    else:
        return render_template("index2.html",arr=[],video=[])



    
