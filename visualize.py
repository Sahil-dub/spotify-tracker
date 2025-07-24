import json
import plotly.express as px
import pandas as pd
from datetime import datetime

# ---------- TOP ARTISTS ----------
with open("data/top_artists.json", "r", encoding="utf-8") as f:
    artists_data = json.load(f)

artist_df = pd.DataFrame(artists_data)
artist_df["genres_str"] = artist_df["genres"].apply(lambda g: ", ".join(g))

fig1 = px.bar(
    artist_df,
    x="name",
    y="popularity",
    hover_data=["followers", "genres_str"],
    labels={"name": "Artist", "popularity": "Popularity"},
    title="Top Artists by Popularity (with Genres and Followers)"
)
fig1.show()

# ---------- TOP GENRES ----------
with open("data/top_genres.json", "r", encoding="utf-8") as f:
    genre_data = json.load(f)

genre_df = pd.DataFrame(genre_data.items(), columns=["Genre", "Count"])
fig2 = px.pie(
    genre_df,
    names="Genre",
    values="Count",
    title="Top Genres Breakdown",
    hover_data=["Count"],
)
fig2.update_traces(textinfo="percent+label")
fig2.show()

# ---------- RECENT TRACKS ----------
with open("data/recent_tracks.json", "r", encoding="utf-8") as f:
    recent_data = json.load(f)

for item in recent_data:
    item["played_at"] = datetime.strptime(item["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

recent_df = pd.DataFrame(recent_data)

fig3 = px.line(
    recent_df,
    x="played_at",
    y=[1] * len(recent_df),  # dummy y
    labels={"played_at": "Timestamp"},
    title="Recent Listening Timeline",
    hover_data=["track_name", "artist"],
)
fig3.update_traces(mode="markers+lines")
fig3.show()
