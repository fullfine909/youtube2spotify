from flask import Flask, redirect, url_for, render_template, request
from sputils import textarea2list, find_songs, createPlaylist
from ytutils import getVideo, getVideoID
from songutils import saveSongs, openRes


application = Flask(__name__)

@application.route("/",methods=["POST","GET"])
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



    
if __name__ == "__main__":
    application.debug = True
    application.run()

