
from flask import render_template, request, redirect, url_for, session  
from FlaskWebProject1 import app
from FlaskWebProject1.apiutil import link2data




@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        if 'goresult' in request.form:
            url = request.form["link_input"] # yt url
            session["url"] = url
            return redirect(url_for("result"))
        elif 'gosql' in request.form:
            return redirect(url_for("sql"))
    else:
        return render_template("home.html")


@app.route("/result",methods=["POST","GET"])
def result():
    if request.method == "POST":
        return redirect(url_for("home"))     
    if 'url' in session:
        url = session['url']  
        [songs,v] = link2data(url)
        # [songs,yt] = openRes()
        return render_template("result.html",arr=songs,video=v)
    else:
        return redirect(url_for("home"))

@app.route("/sql",methods=["POST","GET"])
def sql():
    if request.method == "POST":
        return redirect(url_for("home"))  
    return render_template("sql.html")
