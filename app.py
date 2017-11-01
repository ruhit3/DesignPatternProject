from flask import Flask, render_template, request, json
import pandas as pd
import numpy as np
from math import sqrt
from prediction import pearson, getRecommendations

app = Flask(__name__)

movie_watched = {}

movies = {}
for line in open('u.item'):
    (id, title) = line.split('|')[0:2]
    movies[id] = title[:-7]

prefs = {}
prefs.setdefault('999', {})
for line in open('u.data'):
    (user, movieid, rating, ts) = line.split('\t')
    prefs.setdefault(user, {})
    prefs[user][movies[movieid]] = float(rating)

def getMovieKey(movie_name):
    for key, value in movies.items():
        if value == movie_name:
            return key

def insertPref(user_movie, user_rating):
    prefs['999'][movies[getMovieKey(user_movie)]] = float(user_rating)

movie_predicted = list()

@app.route('/')
def index():
    #return render_template('menu.html')
    return render_template('index.html', movie_watched=movie_watched, movies=movies, dark=False, movie_predicted=movie_predicted)    

@app.route('/', methods=['POST'])
def add():
    global movie_predicted
    if request.form['button'] == 'Add to your watch list':
        movie_name = request.form['movie_name']
        movie_rating = request.form['movie_rating']
        print(movie_rating)
        movie_watched[movie_name] = movie_rating
        insertPref(movie_name, movie_rating)
        return render_template('index.html', movie_watched=movie_watched, movies=movies, dark=False, movie_predicted=movie_predicted)        
    else:
        movie_predicted = getRecommendations(prefs, '999', 5)
        return render_template('index.html', movie_watched=movie_watched, movies=movies, dark=False, movie_predicted=movie_predicted)
        #return '', 204

if __name__ == '__main__':
    app.run(debug=True)