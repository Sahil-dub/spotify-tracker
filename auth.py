import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

scope = "user-top-read user-read-recently-played"

print("Starting Spotify authentication...")

try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=scope
    ))
    print("Authentication successful!")

    results = sp.current_user_top_tracks(limit=10, time_range='short_term')

    for idx, item in enumerate(results['items']):
        print(f"{idx + 1}. {item['name']} by {item['artists'][0]['name']}")

except Exception as e:
    print(f"Error during authentication or data fetch: {e}")
