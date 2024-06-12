from flask import Flask, render_template,flash
from forms import recommendation_form
import pickle
import pandas as pd
import requests
import json
movies_dict = None
movies = None
similarity = None
tmdb_data = None

def fetch_poster(movie_id):
    # response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=20d913bda50836a3a7c9e7ad70acab65&language=en-US")
    # data = response.json()
    # return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return ""

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:19]
    recommended_movies = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append({"id":movie_id, "poster":fetch_poster(movie_id), "title":movies.iloc[i[0]].title})
    return recommended_movies


app = Flask(__name__)
app.config['SECRET_KEY'] = '9f479d5advd024b17588be45'
@app.route('/', methods=['GET', 'POST'])
def home_page():
    rf = recommendation_form()
    rf.movie_name.choices = list(movies['title'])
    if rf.validate_on_submit():
        rec_movies = recommend(rf.movie_name.data)
        return render_template('index.html', form=rf, movies=rec_movies)
    if len(rf.errors) != 0:
        for err_msg in rf.errors.values:
            flash(f'There was an error in creating the user: {err_msg}', category='danger')
    return render_template('index.html', form=rf, movies=None)

@app.route('/desc/<id>', methods=['GET'])
def desc(id):
    my_movie = tmdb_data[tmdb_data['id'] == int(id)].iloc[0]
    movie = dict()
    movie["title"] = my_movie.title
    movie["tagline"] = my_movie.tagline
    movie["vote_average"] = my_movie.vote_average
    movie["overview"] = my_movie.overview
    movie["genres"] = ""
    print(my_movie.genres)
    for genre in json.loads(my_movie.genres):
        movie["genres"] += genre["name"]
        movie["genres"] += ", "
    return render_template('desc.html', movie=movie)

if __name__ == '__main__':
    movies_dict = pickle.load(open('./dataset_web/movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    tmdb_data = pd.read_csv('./dataset_web/tmdb_5000_movies.csv')
    similarity = pickle.load(open('./dataset_web/similarity.pkl', 'rb'))
    app.run(debug=True)

