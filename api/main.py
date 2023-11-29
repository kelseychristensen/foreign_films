import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String)
    year = db.Column(db.Integer)
    seen = db.Column(db.Boolean)
    poster_url = db.Column(db.String)


@app.route("/", methods=["GET", "POST"])
def home():
    movies = db.session.query(Movie).all()
    return render_template('index.html', movies=movies)


@app.route('/pick', methods=["GET", "POST"])
def pick():
    unseen_movies = db.session.query(Movie).filter_by(seen=False).all()
    choice = random.choice(unseen_movies)
    return render_template('picker.html', movie=choice)

@app.route("/mark_watched/<item_id>", methods=["GET", "POST"])
def mark_watched(item_id):
    item_to_complete = db.session.query(Movie).get(item_id)
    if request.method == 'POST':
        item_to_complete.seen = 1
        db.session.commit()
        movies = db.session.query(Movie).all()
        return render_template('index.html', movies=movies)
    return render_template('mark_watched.html', movie=item_to_complete)


if __name__ == '__main__':
    app.run(debug=True)
