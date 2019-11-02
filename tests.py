import requests
from soup_scraper import grab_artist_lyrics
import tqdm


def test_base_connection_valid():
    base_url = 'http://www.metrolyrics.com/'
    assert requests.get(base_url).status_code == 200
