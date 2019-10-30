import time
import os
import re
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as soup

base_url = 'http://www.metrolyrics.com/'

def grab_artist_lyrics(x):
    artist_names = []
    for each in x:
        artist = each.lower().strip().split(' ')
        artist_path = '-'.join(artist) + '-lyrics.html'
        artist_name = '_'.join(artist)
        artist_names.append(artist_name)
        path = base_url + artist_path
        all_songs = requests.get(path)
        all_songs_bs4 = soup(all_songs.text, 'html.parser')
        results = all_songs_bs4.find_all(attrs = {'class':'songs-table compact'})[0]
        songs = results.find_all('a')
        artist_urls = []
        for i in range(len(songs)):
            artist_urls.append(songs[i].get('href'))
        regex = r'https:\/\/www\.metrolyrics\.com\/(\S+)'
        song_names = []
        for each in artist_urls:
            song = re.findall(regex, each)[0]
            song = song.split('-')
            artist_size = len(artist) + 1
            song = song[:-artist_size]
            song = '_'.join(song)
            song = artist_name + '_' + song
            song_names.append(song)
        for i in tqdm(range(5), ascii=True, desc=f"saving {artist_name}'s files"):
            song = requests.get(artist_urls[i])
            song1 = soup(song.text, 'html.parser')
            song_lyrics = song1.find_all(attrs={'class':'js-lyric-text'})[0]
            s2= song_lyrics.find_all('p')
            lyrics = ''
            for each in s2:
                lyrics += each.text
            clean_lyrics = re.sub('[\n\-\?\.\,\(\)]', ' ', lyrics)
            clean_lyrics = re.sub('[\']', '', clean_lyrics)
            file = '/home/tommu/code/spiced/scrape_nlp/' + song_names[i] + '.txt'
            with open(file,'w') as f:
                f.write(lyrics)
    return artist_names
