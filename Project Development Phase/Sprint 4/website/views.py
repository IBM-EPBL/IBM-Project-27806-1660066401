from flask import Blueprint, render_template
from flask_login import login_required, current_user
import requests
import json
from .credentials import api_key


views = Blueprint("views", __name__)


@views.route('/', defaults = {'topic' : None})
@views.route('/<topic>')
@login_required
def home(topic):
    if topic:
        url = "https://api.newscatcherapi.com/v2/latest_headlines"
        extension = "?topic=" + topic
        url = url + extension
        print(url)
    else:
        url = "https://api.newscatcherapi.com/v2/latest_headlines"
    querystring = {"lang": "en"}
    headers = {
        "x-api-key": api_key
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    # print(data)


    return render_template("home.html", user = current_user, topic = topic, data = data["articles"])
