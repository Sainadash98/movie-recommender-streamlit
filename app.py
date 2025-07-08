import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# Download movie_dict.pkl from Google Drive
movie_dict_url = "https://drive.google.com/uc?id=1JGcxT-D3_OGVQOxeDn5U3KxCAKxteRqi"
movie_dict_file = "movie_dict.pkl"
if not os.path.exists(movie_dict_file):
    gdown.download(movie_dict_url, movie_dict_file, quiet=False)

# Download similarity.pkl from Google Drive
similarity_url = "https://drive.google.com/uc?id=1Mowj6_InscJMD1hGpcJ1A-y5B6K0LcvJ"
similarity_file = "similarity.pkl"
if not os.path.exists(similarity_file):
    gdown.download(similarity_url, similarity_file, quiet=False)

# Download movies.pkl from Google Drive
movies_url = "https://drive.google.com/uc?id=1Bbm8uN4DZwbQvfJfquXWTEOGXTaB3kpm"
movies_file = "movies.pkl"
if not os.path.exists(movies_file):
    gdown.download(movies_url, movies_file, quiet=False)

# Load the pickle files
with open(movie_dict_file, 'rb') as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

with open(similarity_file, 'rb') as f:
    similarity = pickle.load(f)

#def fetch_poster(title):
    #response = requests.get('https://www.omdbapi.com/?t={title}&apikey=56891f43'.format(title))
    #data = response.json()
    #return data['Poster']

def fetch_poster_by_title(title):
    url = f"https://www.omdbapi.com/?t={title}&apikey=56891f43"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster')


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_posters.append(fetch_poster_by_title(title))
    return recommended_movies,recommended_movie_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

    #for i in recommendations:
        #st.write(i)





