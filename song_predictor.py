import time
import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


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
        for i in range(10):
            artist_urls.append(songs[i].get('href'))
        regex = r'http:\/\/www\.metrolyrics\.com\/(\S+)'
        song_names = []
        for each in artist_urls:
            song = re.findall(regex, each)[0]
            song = song.split('-')
            artist_size = len(artist) + 1
            song = song[:-artist_size]
            song = '_'.join(song)
            song = artist_name + '_' + song
            song_names.append(song)
        for i in range(len(artist_urls)):
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
                f.write(clean_lyrics)
    print('-----------------------')
    print('All files saved to disk')
    print('-----------------------')
    time.sleep(0.5)
    return artist_names

def bag_of_words(y):
    all_lyrics = []
    artist_name = []
    path = '/home/tommu/code/spiced/scrape_nlp/'
    for artist in y:
        for file in os.listdir(path):
            if artist in file and '.txt' in file:
                with open(path + file, 'r') as f:
                    all_lyrics.append(f.read())

        artist = [artist] * 10
        artist_name += artist
    artist_name = pd.factorize(artist_name)[0]
    tv = TfidfVectorizer()
    vec_lyrics = tv.fit_transform(all_lyrics)
    print('Song lyrics vectorised')
    print('-----------------------')
    time.sleep(0.5)
    return vec_lyrics, artist_name, tv

def train_my_nb(x,y):
    m = MultinomialNB()
    m.fit(x,y)
    print('Model is trained')
    print('-----------------------')
    time.sleep(0.5)
    return m



if __name__ == '__main__':
    all_artists = []
    all_artists.append(input('input artist no.1:\n'))
    time.sleep(0.5)
    all_artists.append(input('input artist no.2:\n'))
    clean_artists = grab_artist_lyrics(all_artists)
    lyrics, names, tv = bag_of_words(clean_artists)
    time.sleep(0.5)
    model = train_my_nb(lyrics,names)
    time.sleep(0.5)
    guess = input('Now paste in a song lyric from one of the artists:\n')
    clean_guess = re.sub('[\n\-\?\.\,\(\)]', ' ', guess)
    clean_guess = re.sub('[\']', '', clean_guess)
    vec_guess = tv.transform([clean_guess])
    prediction = model.predict_proba(vec_guess)
    df = pd.DataFrame(prediction.round(2), columns = all_artists)
    print(df)
