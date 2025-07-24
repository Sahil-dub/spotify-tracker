import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="52688fd34c9e4fc6b33f8af93226dbd5",
    client_secret="cc9fb29990c442b4ac9b5db7aa672eaa",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-top-read user-read-recently-played"
))

print("Starting Spotify authentication...")

results = sp.current_user_top_tracks(limit=10, time_range='medium_term')

print("Authentication successful!")
for idx, item in enumerate(results['items']):
    print(f"{idx + 1}. {item['name']} by {item['artists'][0]['name']}")
