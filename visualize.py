import json
import plotly.express as px
import pandas as pd
from datetime import datetime

# Load top artists
with open("data/top_artists.json", "r", encoding="utf-8") as f:
    artist_data = json.load(f)

# Top artists by popularity
artists = [artist['name'] for artist in artist_data['items']]
popularity = [artist['popularity'] for artist in artist_data['items']]

fig = px.bar(x=artists, y=popularity,
             labels={'x': 'Artist', 'y': 'Popularity'},
             title='Top Spotify Artists by Popularity')
fig.show()

# Load genre data
with open("data/top_genres.json", "r", encoding="utf-8") as f:
    genre_data = json.load(f)

genre_df = pd.DataFrame(genre_data.items(), columns=["Genre", "Count"])
genre_df = genre_df.sort_values("Count", ascending=False).head(10)

fig2 = px.pie(genre_df, names="Genre", values="Count", title="Top 10 Genres")
fig2.show()

# Load recent tracks
with open("data/recent_tracks.json", "r", encoding="utf-8") as f:
    recent_data = json.load(f)

timestamps = []
track_names = []

for item in recent_data['items']:
    played_at = item['played_at']
    track_name = item['track']['name']
    dt = datetime.strptime(played_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamps.append(dt)
    track_names.append(track_name)

df = pd.DataFrame({"Time Played": timestamps, "Track": track_names})
df = df.sort_values("Time Played")

fig3 = px.line(df, x="Time Played", y=[1]*len(df), hover_data=["Track"],
               title="Recent Spotify Listening Timeline",
               labels={"y": "Plays"}, markers=True)
fig3.update_traces(line_color='green', showlegend=False)
fig3.update_yaxes(visible=False)
fig3.show()
