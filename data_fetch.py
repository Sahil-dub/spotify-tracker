import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
from dotenv import load_dotenv

load_dotenv()

scope = "user-top-read user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=scope
))

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def fetch_top_artists():
    results = sp.current_user_top_artists(limit=20, time_range='medium_term')
    save_json(results, 'top_artists.json')
    print(f"Saved top artists to top_artists.json")

def fetch_recently_played():
    results = sp.current_user_recently_played(limit=20)
    save_json(results, 'recently_played.json')
    print(f"Saved recently played tracks to recently_played.json")

def extract_genres():
    with open('top_artists.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    genres = []
    for artist in data['items']:
        genres.extend(artist.get('genres', []))
    unique_genres = list(set(genres))
    save_json(unique_genres, 'top_genres.json')
    print(f"Saved extracted genres to top_genres.json")

if __name__ == "__main__":
    fetch_top_artists()
    fetch_recently_played()
    extract_genres()
