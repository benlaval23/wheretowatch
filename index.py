from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from os import environ
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()

app.config["SECRET_KEY"] = "my_secret"

# DBsetup
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
    "DATABASE_URL") or "sqlite:///mmyDB.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Searches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String(100), index=True, unique=False)

class Search(FlaskForm):
    name = StringField("Enter film name", render_kw={
                       "placeholder": "Search a film or series..."})
    submit = SubmitField("")

# APIcall
url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

querystring = {"term": None, "country": "uk"}

headers = {
    'x-rapidapi-key': os.environ['API_KEY_'],
    'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
results_dict = json.loads(response.text)
#APIcall - end

list_of_popular_results = []


@app.route('/', methods=["GET", "POST"])
def home():
    my_form = Search()
    if 'name' in request.form:
        search = request.form['name']
        return redirect(url_for('home', name=search))
    
    search = request.args.get('name')
    if search:
        querystring["term"] = search
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        results_dict = json.loads(response.text)
        list_of_popular_results.append(results_dict['results'])
        results_count = len(results_dict['results'])
        return render_template('index_search.html', template_results=results_dict, template_form=my_form, search=search, results_count=results_count)
    return render_template('index.html', template_form=my_form)
