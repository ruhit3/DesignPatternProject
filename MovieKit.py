from flask import Flask, render_template, request
from Recommendation import getRecommendations
from SentimentAnalysis import getSentiment

server = Flask(__name__)

movie_watched = {}

movies = {}
for line in open('dataset/u.item'):
    (id, title) = line.split('|')[0:2]
    movies[id] = title[:-7]

prefs = {}
prefs.setdefault('999', {})
for line in open('dataset/u.data'):
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

@server.route('/')
def home():
    #load_data
    return render_template('home.html')

@server.route('/getRecommendation', methods=['GET', 'POST'])
def getRecommendation():
    if request.method == 'POST':
        global movie_predicted
        if request.form['button'] == 'Add to watchlist':
            movie_name = request.form['movie_name']
            movie_rating = request.form['movie_rating']
            movie_watched[movie_name] = movie_rating
            insertPref(movie_name, movie_rating)
            return render_template('getRecommendation.html', movie_watched=movie_watched, movies=movies, dark=False, movie_predicted=movie_predicted)        
        elif request.form['button'] == 'Clear':
            movie_watched.clear()
            movie_predicted.clear()
            return render_template('getRecommendation.html', movie_watched=movie_watched, movies=movies, dark=False, movie_predicted=movie_predicted)
        else:
            movie_predicted = getRecommendations(prefs, '999', 3)
            return render_template('getRecommendation.html', movie_watched=movie_watched, movies=movies, dark=False, movie_predicted=movie_predicted)
    else:
        return render_template('getRecommendation.html', movie_watched=movie_watched, movies=movies, dark=False, movie_predicted=movie_predicted)
        

@server.route('/sentimentAnalysis', methods=['GET', 'POST'])
def sentimentAnalysis():
    if request.method == 'POST':
        if request.form['button'] == 'Analyse the review':
            user_review = request.form['textArea']
            flag = getSentiment(user_review)
            return render_template('sentimentAnalysis.html', flag=flag)
        elif request.form['button'] == 'Clear':
            flag = -1
            return render_template('sentimentAnalysis.html', flag=flag)
    else:
        flag = -1
        return render_template('sentimentAnalysis.html', flag=flag)

if __name__ == '__main__':
    server.run(debug=True)
