import streamlit as st
import pickle
import requests


api_key = "YOUR_TMDB_API_KEY"

def fetchPoster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    recommend_movie_names = []
    recommend_movie_images = []
    for i in distances[1: 6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie_images.append(fetchPoster(movie_id))
        recommend_movie_names.append(movies.iloc[i[0]].title)
    return recommend_movie_names, recommend_movie_images

st.header('Movie Recommended System')
movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a Movie',
    movie_list
)

if st.button('Show Recommendations'):
    recommend_movie_names, recommend_movie_images = recommend(selected_movie)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommend_movie_names[i])
            st.image(recommend_movie_images[i])