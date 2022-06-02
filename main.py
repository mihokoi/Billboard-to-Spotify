from bs4 import BeautifulSoup
import requests
import os
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']

desired_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

URL = "https://www.billboard.com/charts/hot-100/"
result = requests.get(f"{URL}{desired_date}").text


soup = BeautifulSoup(result, 'lxml')
song_page = soup.select("li ul li h3")
artists = soup.select("li ul li span")
top_100_list = [song.getText().replace("\n", "").replace("\t", "") for song in song_page]
scrapped_artist = [artist_.getText().replace("\n", "").replace("\t", "") for artist_ in artists]
artist_list =[]
for item in scrapped_artist:
    if not item.isnumeric():
        artist_list.append(item)

print(scrapped_artist)
print(artist_list)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

track_uris=[]
date = desired_date.split("-")[0]

for track, artisto in zip(top_100_list, artist_list):
    x = sp.search(q=f"track:{track} artist:{artisto}, type='track'")
    try:
        uri = x['tracks']['items'][0]['uri']
        track_uris.append(uri)
    except IndexError:
        print(f"{track} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)