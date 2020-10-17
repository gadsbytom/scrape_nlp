"""select how many songs to scrape at a time
catch incorrect artist inputs
allow the user to input more than a sing """

"""This file scrapes lyrics using BS4"""

import time
import os
import re
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as soup
from pyfiglet import Figlet


def compile_artists(banner):
    """user inputs all artists to be scraped, returns those artists"""

    base_url = 'http://www.metrolyrics.com/'
    artist_main_page_url = []
    artist_names = []

    #collect artist names, check they have a url, and stop when 'done' is entered
    print(banner.renderText('INPUT!!\n'))
    i = True
    while i:
        new_artist = input("\nPlease enter an artist's name, or type 'done' to finish:\n\n ")
        if new_artist.strip().lower() == 'done':
            i = False
        else:
            artist = new_artist.lower().strip().split(' ')
            artist_name = '-'.join(artist)
            artist_path = artist_name + '-lyrics.html'
            path = base_url + artist_path
            all_songs = requests.get(path)
            if all_songs:
                artist_names.append(artist_name)
                artist_main_page_url.append(all_songs)
                print(f"\n {new_artist} added!")
                print(f"-------------------------------------------------------------------")
            else:
                print(f"\n OOPS! We can't find '{new_artist}'. Please try again.")
                print(f"-------------------------------------------------------------------")
    time.sleep(0.5)
    return artist_main_page_url, artist_names


def grab_artist_lyrics(artist_links, artist_names, banner):
    """accepts a list of artists, scrapes one page of songs, saves to disk and returns artists names"""

    print(banner.renderText('SCRAPING!!\n'))
    print('\t---Thanks Metrolyrics---\n')
    if not os.path.exists('songs'):
        os.makedirs('songs')

    #loop over each inputted artist, make a directory, and generate song names and song url lists
    for i, artist_link in enumerate(artist_links):
        if not os.path.exists(f'songs/{artist_names[i]}'):
            os.makedirs(f'songs/{artist_names[i]}')
        base_url = 'http://www.metrolyrics.com/'
        regex = r'https:\/\/www\.metrolyrics\.com\/(\S+)'
        song_urls = []
        song_names = []
        all_songs_bs4 = soup(artist_link.text, 'html.parser')
        results = all_songs_bs4.find_all(attrs = {'class':'songs-table compact'})[0]
        song_links = results.find_all('a')

        for j, link in enumerate(song_links):
            song_url = link.get('href')
            song_urls.append(song_url)

            song_name = re.findall(regex, song_url)[0]
            song_name = song_name.split('-')
            song_name = '_'.join(song_name)
            song_name = song_name[:-5]
            song_names.append(song_name)

        #for each song url, pull out all the text and save it in a txt file
        for k in tqdm(range(len(song_urls)), ascii=True, desc=f"saving {artist_names[i]}'s files"):
            try:
                page = requests.get(song_urls[k])
                song = soup(page.text, 'html.parser')
                song_lyrics = song.find_all(attrs={'class':'js-lyric-text'})[0]
                s2= song_lyrics.find_all('p')
                lyrics = ''
                for each in s2:
                    lyrics += each.text
                clean_lyrics = re.sub(r'[\n\-\?\.\,\(\)] | [\']', ' ', lyrics)
                file = f'./songs/{artist_names[i]}' + '/' + song_names[k] + '.txt'
                with open(file,'w') as f:
                    f.write(clean_lyrics)
            except:
                continue

    print("\n ------------------------------------------------------------")
    print("files are now saved in the folder named '/songs'")
    return artist_names
