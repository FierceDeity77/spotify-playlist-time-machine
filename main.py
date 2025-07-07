from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("E-CLIENT-ID")
SPOTIFY_CLIENT_SECRET = os.getenv("E-CLIENT-SECRET")
SPOTIFY_TOKEN = os.getenv("E-SPOTIFY-TOKEN")
URL = "https://www.billboard.com/charts/hot-100/2000-08-12"
SPOTIFY_SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"

# created an object from Spotify class with required parameters for lib init
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private"))

username = sp.current_user()["id"]

date = input("what year would you like to travel? type the date in this yyyy-mm-dd format: ")
year = date.split("-")[0]

# calls a method to create a playlist
playlist = sp.user_playlist_create(user=username, name=f"{year}'s Billboard 100", public=False, collaborative=False,
                                   description="Playlist created from python code")
playlist_id = playlist["id"]

# scraping billboard 100
response = requests.get(URL)
top_songs = response.text
soup = BeautifulSoup(top_songs, "html.parser")
all_songs = soup.select(selector="li .c-title")
song_names = [song.getText().strip() for song in all_songs]

all_track_uri = []
for title in song_names:
    sp_params = {
        "q": f"{year}, {title}",
        "type": "track",
        "limit": 1
    }
    auth_parameters = {
        "Authorization": f"Bearer {SPOTIFY_TOKEN}"
    }
    sp_response = requests.get(SPOTIFY_SEARCH_ENDPOINT, headers=auth_parameters, params=sp_params)
    track = sp_response.json()["tracks"]["items"][0]["uri"][14:]
    all_track_uri.append(track)

sp.playlist_add_items(playlist_id=playlist_id, items=all_track_uri, position=None)








