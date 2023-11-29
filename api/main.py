import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import random
import json


app = Flask(__name__)
Bootstrap(app)

path = 'api/static/movies.json'


@app.route("/", methods=["GET", "POST"])
def home():
    with open(path, 'r') as file:
        movies = json.load(file)
    return render_template('index.html', movies=movies)


@app.route('/pick', methods=["GET", "POST"])
def pick():
    with open(path, 'r') as file:
        movies = json.load(file)
    unseen_movies = [movie for movie in movies if movie["seen"]=="False"]
    choice = random.choice(unseen_movies)
    return render_template('picker.html', movie=choice)

@app.route("/mark_watched/<item_id>", methods=["GET", "POST"])
def mark_watched(item_id):
    with open(path, 'r') as file:
        movies = json.load(file)
    item_to_complete = movies[int(item_id)]
    if request.method == 'POST':
        with open(path, 'r') as file:
            movies = json.load(file)
        movies[int(item_id)]['seen'] = "True"
        with open(path, 'w') as file:
            json.dump(movies, file, indent=4)
        return render_template('index.html', movies=movies)
    return render_template('mark_watched.html', movie=item_to_complete, item_id=item_id)


if __name__ == '__main__':
    app.run(debug=True)