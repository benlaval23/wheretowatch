from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from os import environ

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret"

# DBsetup
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
    "DATABASE_URL") or "sqlite:///mmyDB.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Searches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String(100), index=True, unique=False)

# db.create_all()
#DBsetup - end

# FORMsetup


class Search(FlaskForm):
    name = StringField("Enter film name", render_kw={
                       "placeholder": "Search a film or series..."})
    submit = SubmitField("")
#FORMsetup - end


# APIcall
url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

querystring = {"term": None, "country": "uk"}

headers = {
    'x-rapidapi-key': "53b02ccf6amsha7b882872db07dep11f9afjsndddc84797880",
    'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
results_dict = json.loads(response.text)
#APIcall - end


@app.route('/', methods=["GET", "POST"])
def home():
    my_form = Search()
    if 'name' in request.form:
        search = request.form['name']
        querystring["term"] = search
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        results_dict = json.loads(response.text)
        results_count = len(results_dict['results'])
        return render_template('index_search.html', template_results=results_dict, template_form=my_form, search=search, results_count=results_count)
    return render_template('index.html', template_form=my_form)

# for result in results_dict['results']:
#  print(result['name'])
#  for location in result['locations']:
#    print(location['display_name'])
#    print(location['url'])
