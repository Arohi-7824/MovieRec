import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()

    return {
        "poster": f"https://image.tmdb.org/t/p/w500/{data.get('poster_path')}" if data.get("poster_path") else None,
        "overview": data.get("overview", "No overview available."),
        "rating": data.get("vote_average", "N/A"),
        "year": data.get("release_date", "")[:4],
        "genres": [g["name"] for g in data.get("genres", [])]
    }


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()

    if data.get("poster_path"):
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return None


def recommend(movie, movies, similarity):
    idx = movies[movies["title"] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names, posters = [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters
