from flask import Flask, redirect, url_for, render_template, request
from sputils import textarea2list, find_songs
from ytutils import getVideo, getVideoID
from songutils import saveSongs, openRes
app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        url = request.form["link_input"]        # yt url
        video =  getVideo(url)                  # dict video with info
        songs_list = textarea2list(video)       # get tracklist from comments of video
        songs = find_songs(songs_list)          # songs found in spotify
        saveSongs(songs,video)                  # add songs to sql database
        # [songs,yt] = openRes()
        return render_template("index2.html",arr=songs,yt=video["title"])
    else:
        return render_template("index2.html",arr=[],yt=[])

    
if __name__ == "__main__":
    app.debug = True
    app.run()

