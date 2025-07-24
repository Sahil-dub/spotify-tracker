import streamlit as st
import json
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Spotify Tracker", layout="wide")

st.title("🎵 Spotify Tracker Dashboard")

# Load data
with open("data/top_artists.json", "r", encoding="utf-8") as f:
    artist_data = json.load(f)
artist_df = pd.DataFrame(artist_data)
artist_df["genres_str"] = artist_df["genres"].apply(lambda g: ", ".join(g))

with open("data/top_genres.json", "r", encoding="utf-8") as f:
    genre_data = json.load(f)
genre_df = pd.DataFrame(genre_data.items(), columns=["Genre", "Count"])

with open("data/recent_tracks.json", "r", encoding="utf-8") as f:
    recent_data = json.load(f)
for item in recent_data:
    item["played_at"] = datetime.strptime(item["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
recent_df = pd.DataFrame(recent_data)

# Sidebar filters
page = st.sidebar.radio("📂 Select View", ["Top Artists", "Top Genres", "Listening Timeline"])

# Date filter for recent tracks
min_date = recent_df["played_at"].min().date()
max_date = recent_df["played_at"].max().date()
date_range = st.sidebar.date_input("Filter recent tracks by date", [min_date, max_date])

# Artist filter for recent tracks
unique_artists = recent_df["artist"].unique().tolist()
selected_artists = st.sidebar.multiselect("Filter recent tracks by artist", options=unique_artists, default=unique_artists)

# Filter recent_df based on inputs
filtered_recent_df = recent_df[
    (recent_df["played_at"].dt.date >= date_range[0]) &
    (recent_df["played_at"].dt.date <= date_range[1]) &
    (recent_df["artist"].isin(selected_artists))
]

if page == "Top Artists":
    st.subheader("🎤 Top Artists by Popularity")
    fig1 = px.bar(
        artist_df,
        x="name",
        y="popularity",
        hover_data=["followers", "genres_str"],
        labels={"name": "Artist", "popularity": "Popularity"},
    )
    st.plotly_chart(fig1, use_container_width=True)

elif page == "Top Genres":
    st.subheader("🎧 Genre Distribution")
    fig2 = px.pie(
        genre_df,
        names="Genre",
        values="Count",
        title="Top Genres Breakdown",
        hover_data=["Count"],
    )
    fig2.update_traces(textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Listening Timeline":
    st.subheader("📅 Recent Listening Timeline")
    # Show timeline of filtered data
    fig3 = px.line(
        filtered_recent_df,
        x="played_at",
        y=[1] * len(filtered_recent_df),  # dummy y
        labels={"played_at": "Timestamp"},
        hover_data=["track_name", "artist"],
    )
    fig3.update_traces(mode="markers+lines")
    fig3.update_yaxes(visible=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("🏆 Top 10 Most Played Songs (Filtered)")
    # Count top songs in filtered data
    top_songs = (
        filtered_recent_df["track_name"]
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={"index": "Track", "track_name": "Play Count"})
    )
    fig4 = px.bar(
        top_songs,
        x="Track",
        y="Play Count",
        labels={"Track": "Track Name", "Play Count": "Times Played"},
        title="Top 10 Most Played Songs"
    )
    st.plotly_chart(fig4, use_container_width=True)
