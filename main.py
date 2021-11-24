from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=URL)
soup = BeautifulSoup(response.text, "html.parser")

song_titles = soup.select("li ul h3")
song_names = [each_song.getText().strip() for each_song in song_titles]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR CLIENT ID",
    client_secret="YOUR CLIENT SECRET",
    redirect_uri="http://example.com",
    scope="playlist-modify-private",
    cache_path="token.txt"
))

user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} -- skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
