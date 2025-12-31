import streamlit as st
import pickle
from utils import recommend, fetch_movie_details

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = ""

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="MovieRec", layout="wide")

# ---------------- LOAD DATA ------------------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# ---------------- CSS ------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1a1a2e, #0b0b12);
    color: white;
}

h1 {
    color: #a855f7;
    font-size: 3rem;
}

.hero {
    text-align: center;
    margin-top: 120px;
    opacity: 0.9;
}

.hero h2 {
    font-size: 2.2rem;
}

.hero p {
    color: #9ca3af;
    font-size: 1rem;
}

.badge {
    display: inline-block;
    background-color: #312e81;
    color: #c4b5fd;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    margin-right: 6px;
}

.movie-card {
    background: linear-gradient(145deg, #1f1f2e, #11111b);
    border-radius: 20px;
    padding: 24px;
}

img {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------------
st.markdown("<h1>MovieRec</h1>", unsafe_allow_html=True)
st.write("Discover movies you'll love with AI-powered recommendations")

# ---------------- SEARCH ---------------------
selected_movie = st.selectbox(
    "",
    [""] + list(movies["title"].values),
    index=(
        movies["title"].tolist().index(st.session_state.selected_movie) + 1
        if st.session_state.selected_movie in movies["title"].values
        else 0
    ),
    format_func=lambda x: "Search movies by title, genre, or year..." if x == "" else x
)

if selected_movie != "":
    st.session_state.selected_movie = selected_movie


# ---------------- STATE 1: HERO ----------------
if selected_movie == "":
    st.markdown("""
    <div class="hero">
        <h2>🎬 Start Your Discovery</h2>
        <p>
            Search for any movie above to get personalized recommendations
            based on AI-powered similarity analysis.<br>
            Click on any recommended movie to explore more options.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- STATE 2: MOVIE SELECTED ------
else:
    movie_id = movies[movies["title"] == selected_movie].movie_id.values[0]
    details = fetch_movie_details(movie_id)

    st.markdown(f"✔ Selected: **{selected_movie}**")

    col1, col2 = st.columns([1, 2])

    with col1:
        if details["poster"]:
            st.image(details["poster"], width=300)

    with col2:
        st.markdown(f"<div class='movie-card'><h2>{selected_movie}</h2>", unsafe_allow_html=True)

        for g in details["genres"]:
            st.markdown(f"<span class='badge'>{g}</span>", unsafe_allow_html=True)

        st.markdown(
            f"<p><strong>⭐ {details['rating']}/10</strong> &nbsp;&nbsp; {details['year']}</p>",
            unsafe_allow_html=True
        )

        st.markdown(f"<p>{details['overview']}</p></div>", unsafe_allow_html=True)

    st.markdown("## Recommended For You")
    st.write(f"Based on **{selected_movie}**, here are movies you might enjoy")

    names, posters = recommend(selected_movie, movies, similarity)
    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            if poster:
                st.image(poster, width=180)

            if st.button(name, key=name):
                st.session_state.selected_movie = name
                st.rerun()
