from flask_oauthlib.client import OAuth
from webapp import app
from flask import session, redirect, request, render_template
import json, pymysql, os, ssl, urllib

ssl._create_default_https_context = ssl._create_unverified_context

site = os.environ['SITE']
api = os.environ['API']
db_creds = {
    'password': os.environ['MYSQL_ROOT_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE'],
    'host': os.environ['MYSQL_HOSTNAME'],
    'user': os.environ['MYSQL_USER']
}
oauth = OAuth()
faforever = oauth.remote_app('faforever',
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    base_url=api+"/oauth/authorize",
    access_token_url=api+"/oauth/token",
    request_token_params={"scope":"public_profile"}
)

@app.route("/")
def root():
    return render_template("home.html")

@app.route("/login")
def login():
    return faforever.authorize(callback=site+"/oauth")


@app.route('/oauth',methods=["GET","POST"])
def test3():
    resp = faforever.authorized_response()
    if resp is None:
        return redirect("/fail")
    token = resp["access_token"]
    session['token'] = token

    return redirect("/vote")

@app.route('/vote',methods=["GET","POST"])
def vote():
    if request.method == "POST":
        token = session.get("token")
        if not token:
            return redirect("/fail")
        req = urllib.request.Request(api + "/players/me", method="GET",
            headers={"Authorization":"Bearer " + token})
        with urllib.request.urlopen(req) as response:
            vid = json.loads(response.read().decode('utf8'))["data"]["id"]

        candidate = request.form.get("candidate")
        if not candidate:
            return redirect("/fail")

        conn = pymysql.connect(**db_creds)
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM votes WHERE vid=%s",(vid))
            cursor.execute("INSERT INTO votes VALUES(%s,%s)",(vid,candidate))
        conn.commit()
        conn.close()
        return "Thanks for voting!"

    token = session.get("token")
    if not token:
        return redirect("/fail")

    return render_template("vote.html")


@app.route('/fail')
def fail():
    return "Something went wrong... :("
