import datetime as dt
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

time = input("Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{time}"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
song_titles_span = soup.findAll(name="span", class_="chart-element__information__song text--truncate color--primary")
song_titles = [song_title.getText() for song_title in song_titles_span]
print(song_titles)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_SECRET_ID",
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = []

for song_title in song_titles:
    results = sp.search(q=song_title, limit=1)
    try:
        for idx, track in enumerate(results['tracks']['items']):
            uri = idx, track['uri']
            song_uris.append(uri[1])
    except Exception:
        print("Doesn't exists")

print(song_uris)
playlist = sp.user_playlist_create(user=user_id, name=f"{time} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)