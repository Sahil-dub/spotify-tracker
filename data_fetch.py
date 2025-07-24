import json
from auth import sp

# Top Artists
top_artists = sp.current_user_top_artists(limit=10, time_range="medium_term")

artist_data = []
for artist in top_artists['items']:
    artist_data.append({
        'name': artist['name'],
        'popularity': artist['popularity'],
        'genres': artist['genres'],
        'followers': artist['followers']['total']
    })

with open("data/top_artists.json", "w", encoding="utf-8") as f:
    json.dump(artist_data, f, indent=2)

# Top Genres
genre_count = {}
for artist in artist_data:
    for genre in artist['genres']:
        genre_count[genre] = genre_count.get(genre, 0) + 1

with open("data/top_genres.json", "w", encoding="utf-8") as f:
    json.dump(genre_count, f, indent=2)

# Recent Tracks
recent_tracks = sp.current_user_recently_played(limit=20)
recent_data = []
for item in recent_tracks['items']:
    track = item['track']
    recent_data.append({
        'track_name': track['name'],
        'artist': track['artists'][0]['name'],
        'played_at': item['played_at']
    })

with open("data/recent_tracks.json", "w", encoding="utf-8") as f:
    json.dump(recent_data, f, indent=2)

print("✅ Data updated successfully.")
