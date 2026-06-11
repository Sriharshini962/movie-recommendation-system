import streamlit as st
import pandas as pd
import ast

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge datasets
credits.rename(columns={"movie_id": "id"}, inplace=True)
movies = movies.merge(credits, on="id")

# Keep required columns
movies = movies[
    [
        "id",
        "title_x",
        "overview",
        "genres",
        "cast",
        "crew",
        "release_date",
        "vote_average"
    ]
]

movies.rename(columns={"title_x": "title"}, inplace=True)
movies.dropna(inplace=True)

# ---------------- HELPER FUNCTIONS ----------------
def convert(obj):
    try:
        return [i["name"] for i in ast.literal_eval(obj)]
    except:
        return []

def convert_cast(obj):
    try:
        return [i["name"] for i in ast.literal_eval(obj)[:3]]
    except:
        return []

def fetch_director(obj):
    try:
        return [i["name"] for i in ast.literal_eval(obj) if i["job"] == "Director"]
    except:
        return []

# ---------------- PROCESS DATA ----------------
movies["genres"] = movies["genres"].apply(convert)
movies["cast"] = movies["cast"].apply(convert_cast)
movies["crew"] = movies["crew"].apply(fetch_director)

all_genres = sorted(set(g for sub in movies["genres"] for g in sub))

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#7E22CE;font-size:55px;'>
    🎬 Movie Recommendation System
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style='text-align:center;color:#6B7280;'>
    🍿 Discover Movies by Search or Genre
    </h4>
    """,
    unsafe_allow_html=True
)

st.info("🍿 Welcome! Discover amazing movies by searching or browsing genres.")

# ---------------- STATS ----------------
col1, col2 = st.columns(2)

with col1:
    st.metric("🎬 Total Movies", len(movies))

with col2:
    st.metric("🎭 Genres", len(all_genres))

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎥 Navigation")

choice = st.sidebar.radio(
    "Choose Option",
    ["🔍 Search Movie", "🎯 Filter by Genre"]
)

# ---------------- SEARCH MOVIE ----------------
if choice == "🔍 Search Movie":

    movie_name = st.text_input("Enter Movie Name")

    if st.button("Search"):

        if movie_name.strip():

            result = movies[
                movies["title"].str.lower().str.contains(
                    movie_name.lower(),
                    na=False
                )
            ]

            if not result.empty:

                st.subheader("🎬 Matching Movies")

                for _, row in result.head(10).iterrows():

                    st.markdown(
                        f"""
                        <div style="
                        background-color:#F3E8FF;
                        padding:18px;
                        border-radius:15px;
                        margin-bottom:15px;
                        border:2px solid #A855F7;
                        box-shadow:0 4px 8px rgba(0,0,0,0.1);">

                        <h3 style="color:#7E22CE;">
                        🎥 {row['title']}
                        </h3>

                        <p><b>📅 Release Date:</b> {row['release_date']}</p>
                        <p><b>⭐ Rating:</b> {row['vote_average']}</p>
                        <p><b>🎬 Director:</b> {', '.join(row['crew']) if row['crew'] else 'N/A'}</p>
                        <p><b>👥 Cast:</b> {', '.join(row['cast']) if row['cast'] else 'N/A'}</p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                st.warning("Movie not found 😢")

# ---------------- FILTER BY GENRE ----------------
else:

    genre = st.selectbox("Select Genre", all_genres)

    filtered = movies[
        movies["genres"].apply(lambda x: genre in x)
    ]

    st.subheader(f"🍿 Movies in {genre}")

    for _, row in filtered.head(20).iterrows():

        st.markdown(
            f"""
            <div style="
            background-color:#F3E8FF;
            padding:18px;
            border-radius:15px;
            margin-bottom:15px;
            border:2px solid #A855F7;
            box-shadow:0 4px 8px rgba(0,0,0,0.1);">

            <h3 style="color:#7E22CE;">
            🎥 {row['title']}
            </h3>

            <p><b>📅 Release Date:</b> {row['release_date']}</p>
            <p><b>⭐ Rating:</b> {row['vote_average']}</p>
            <p><b>🎬 Director:</b> {', '.join(row['crew']) if row['crew'] else 'N/A'}</p>

            </div>
            """,
            unsafe_allow_html=True
        )