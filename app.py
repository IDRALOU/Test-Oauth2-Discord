from flask import Flask, session, request
from colorama import init
from requests_oauthlib import OAuth2Session
import requests
import os

init(convert=True)

client_id = ""
client_secret = ""
scope = "identify"
redirect_uri = ""
token_url = "https://discord.com/api/oauth2/token"
authorize_url = "https://discord.com/api/oauth2/authorize"
base_api = "https://discord.com/api"

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def home():
    oauth2 = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth2.authorization_url(authorize_url)
    session["state"] = state
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                nav.menu-nav1 ul li{
                    list-style-type: none;
                    display: inline-block;
                }

                nav.menu-nav1 ul li.btn-1{
                    padding-left: 575px;
                    padding-top: 100px;
                    font-size: 20px;
                }

                nav.menu-nav1 ul li.btn-1 a{
                    text-decoration: none;
                    color: black;
                    background-color: #33B5FF;
                    padding: 7px;
                }

                nav.menu-nav1 ul li.btn-1:hover a{
                    color: #33B5FF;
                    background-color: white;
                    transition: 0.5s all;
                }
            </style>
            <title>
                Test OAuth2 avec Discord
            </title>
            <meta charset="utf-8">
        </head>
        <body>
            <nav class="menu-nav1">
                <ul>
                    <li class="btn-1">
    """ + f"""
                        <a href="{login_url}">
                            Se connecter avec Discord
                        </a>
                    </li>
                </ul>
            </nav>
        </body>
    </html>
    """


@app.route("/profile")
def profile():
    code = request.args.get("code")
    r = requests.post(token_url, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': scope
    })
    access_token = r.json()['access_token']
    r1 = requests.get(f"{base_api}/users/@me", headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"})
    return f"Salut {r1.json()['username']}#{r1.json()['discriminator']} ({r1.json()['id']}) !"

if __name__ == "__main__":
    app.run()
