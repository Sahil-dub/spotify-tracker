import json
import spotipy
from collections import Counter
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-top-read user-read-recently-played"
))

# Create data folder if it doesn't exist
import os
os.makedirs("data", exist_ok=True)

# Fetch top artists
top_artists = sp.current_user_top_artists(limit=20, time_range='medium_term')
with open("data/top_artists.json", "w", encoding="utf-8") as f:
    json.dump(top_artists, f, indent=4)

# Extract and count genres
all_genres = []
for artist in top_artists['items']:
    all_genres.extend(artist['genres'])

genre_counts = Counter(all_genres)
with open("data/top_genres.json", "w", encoding="utf-8") as f:
    json.dump(dict(genre_counts), f, indent=4)

# Fetch recently played tracks
recent_tracks = sp.current_user_recently_played(limit=50)
with open("data/recent_tracks.json", "w", encoding="utf-8") as f:
    json.dump(recent_tracks, f, indent=4)

print("Data fetching complete.")
