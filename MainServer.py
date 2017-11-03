import Facade
from Recommendation import getRecommendations
from SentimentAnalysis import getSentiment
from flask import Flask, render_template, request

#initializing server
server = Flask(__name__)

#loading datasets and objects
app = Facade.Moviekit()
app.start_app()

#initializing global variables
movie_watched = {}
movie_predicted = []
movieListObject = app.database.movie_list
preferenceDictionary = app.database.preferences

#adding dummy user with id='999'
preferenceDictionary.setdefault('999', {})

#creating necessary dictionaries
movies = {}
movie_genre_dict = {}
for mov in movieListObject:
    movies[mov.id] = mov.name
    movie_genre_dict[mov.name] = mov.genre

#custom function
def addToPreference(user_movie, user_rating):
    preferenceDictionary['999'][user_movie] = float(user_rating)

#routes start here
@server.route('/')
def home():
    return render_template('home.html')

@server.route('/getRecommendation', methods=['GET', 'POST'])
def getRecommendation():
    if request.method == 'POST':
        global movie_predicted
        if request.form['button'] == 'Add to watchlist':
            movie_name = request.form['movie_name']
            movie_rating = request.form['movie_rating']
            movie_watched[movie_name] = movie_rating
            addToPreference(movie_name, movie_rating)
            return render_template('getRecommendation.html', movies=movies, movie_genre_dict=movie_genre_dict, movie_watched=movie_watched, movie_predicted=movie_predicted)        
        elif request.form['button'] == 'Clear':
            movie_watched.clear()
            movie_predicted.clear()
            return render_template('getRecommendation.html', movies=movies, movie_genre_dict=movie_genre_dict, movie_watched=movie_watched, movie_predicted=movie_predicted)        
        else:
            movie_predicted = getRecommendations(preferenceDictionary, '999', 5)
            return render_template('getRecommendation.html', movies=movies, movie_genre_dict=movie_genre_dict, movie_watched=movie_watched, movie_predicted=movie_predicted)        
    else:
        return render_template('getRecommendation.html', movies=movies, movie_genre_dict=movie_genre_dict, movie_watched=movie_watched, movie_predicted=movie_predicted)
        
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

#starting server
if __name__ == '__main__':
    server.run(debug=True)