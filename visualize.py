import json
import plotly.express as px

# Load top artists data
with open('top_artists.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract artist names and popularity
artists = [artist['name'] for artist in data['items']]
popularity = [artist['popularity'] for artist in data['items']]

# Create bar chart
fig = px.bar(x=artists, y=popularity,
             labels={'x': 'Artist', 'y': 'Popularity'},
             title='Top Spotify Artists by Popularity')

fig.show()
