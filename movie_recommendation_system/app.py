import streamlit as st
import pandas as pd
import pickle
import requests
import os

# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bdcfdff8a708cba2d3370562375c2a36&language=en-US"
        response = requests.get(url)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except:
        return "https://via.placeholder.com/150x225?text=No+Image"

# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

# Get the base path of the app.py file
base_path = os.path.dirname(os.path.abspath(__file__))

# Load the movie data and similarity matrix
movie_dict_path = os.path.join(base_path, 'movie_dict.pkl')
similarity_path = os.path.join(base_path, 'similarity.pkl')

with open(movie_dict_path, 'rb') as f:
    movie_dict = pickle.load(f)

with open(similarity_path, 'rb') as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movie_dict)

# Streamlit UI
st.title('🎬 Movie Recommendation System')

option = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend Movie'):
    names, posters = recommend(option)

    cols = st.columns(5)
    for idx in range(5):
        with cols[idx]:
            st.text(names[idx])
            st.image(posters[idx])
