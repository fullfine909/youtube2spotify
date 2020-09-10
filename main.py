from flask import Flask, redirect, url_for, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '5a170e03cdce4c0ba9a68a1619a0bf8a'
client_secret = '0fcc2a96ee4a4709b7f911902ccbf079'
auth_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

app = Flask(__name__)

def getSpotifyNames(songs_input):

    def checkline(x):
    
        x = x[:-1]
        x = x.lower()
        x = x.replace(':','')
        x = x.replace('-','')
        x = x.replace('& ','')
        x = x.replace('feat','')
        x = x.replace('.','')
        x = x.replace('(original mix)','')
        # delete collection
        p = x.rfind('[')
        if p > 0:
            x = x[:p-1]

        x = x.split()
        x.pop(0)
        song = ' '.join(x)
        # delte id - id
        if song == 'id id':
            song = ''

        return song

    

    songs_input = songs_input.replace('\r','')
    songs_input = songs_input.split('\n')

    songs = []
    for x in songs_input:
        songs.append(checkline(x))

    songsfound = []
    songsmissed = []
    for x in songs:
        result = sp.search(x,type='track',limit=1)
        if (len(result['tracks']['items']) > 0):
            name = result['tracks']['items'][0]['name']
            artist = result['tracks']['items'][0]['artists'][0]['name']
            songsfound.append(artist+' - '+name)
        else:
            songsmissed.append(x)

    return songsfound


@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        txt = request.form["nm"]
        songsfound = getSpotifyNames(txt)
        return render_template("index.html",arr=songsfound)
    else:
        return render_template("index.html",arr=["a"])

    
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()

