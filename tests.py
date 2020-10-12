import requests
from scrape_songs_with_bs4 import grab_artist_lyrics

def test_base_connection_valid():
    base_url = 'http://www.metrolyrics.com/'
    assert requests.get(base_url).status_code == 200

def test_bad_artists_refused():
    base_url = 'http://www.metrolyrics.com/'
    assert requests.get(base_url).status_code == 200
