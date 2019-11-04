"""This is the primary file for handling new song inputs"""


import time
import os
import re
import pandas as pd
import sys
from pyfiglet import Figlet
from tqdm import tqdm
import numpy as np
from bow import bag_of_words
from soup_scraper import grab_artist_lyrics
from naive_bayes import train_my_nb


def render_welcome(banner):
    print(banner.renderText('GUESS THE LYRICS!!'))
    time.sleep(1)
    print("-------------------v1.0 - Author - lyonne19---------------------")
    print()
    for i in range(2):
        time.sleep(0.5)
    print(" This app will scrape songs for as many artists as you like!")
    print("------------------------------------------------------------")
    time.sleep(1)
    print(" Then train a Naive Bayes model to recognise their lyrics!")
    print("------------------------------------------------------------")
    time.sleep(1)
    print(" Then you can test how well it has learnt the artists' lyrics!")
    print("------------------------------------------------------------")
    time.sleep(1)
    print()

def input_artists():
    all_artists = []
    i = True
    while i:
        artist = input("\n Input:\n Please enter an artist's name, or type 'done' to finish:\n\n ")
        if artist.strip().lower() == 'done':
            i = False
        else:
            all_artists.append(artist)
            print(f"\n {artist} added!")
    time.sleep(0.5)
    return all_artists

def guess_artist(guess, tv, model):
    clean_guess = re.sub('[\n\-\?\.\,\(\)]', ' ', guess)
    clean_guess = re.sub('[\']', '', clean_guess)
    clean_guess = [clean_guess]
    vec_guess = tv.transform(clean_guess)
    prediction = model.predict_proba(vec_guess)
    return prediction



if __name__ == '__main__':
    banner = Figlet(font='slant')
    render_welcome(banner)
    all_artists = input_artists()
    print(all_artists)
    clean_artists = grab_artist_lyrics(all_artists)
    print()
    print("------------------------------------------------------------")
    print('All files saved to disk')
    print()
    lyrics, names, tv = bag_of_words(clean_artists)
    print("------------------------------------------------------------")
    print('Song lyrics vectorised')
    print()
    time.sleep(0.5)
    model = train_my_nb(lyrics,names)
    print("------------------------------------------------------------")
    print('Model is trained')
    print()
    time.sleep(1)
    guess_loop = True
    while guess_loop:
        guess = input(f'\n Now paste in a song lyric from one of your artists, or type 'finish' to finish::\n ")
        prediction = guess_artist(guess, tv, model)
        print("------------------------------------------------------------")
        print('This looks like a song from:')
        time.sleep(1)
        print(banner.renderText(clean_artists[prediction.argmax()]))
        df = pd.DataFrame(prediction.round(2), columns = all_artists)
        time.sleep(1)
        print("------------------------------------------------------------")
        print('And the certainty of the guess is:')
        print(df)

        artist = input("\n Input:\n Please enter an artist's name, or type 'done' to finish:\n\n ")
        if artist.strip().lower() == 'done':
            i = False
        else:
            all_artists.append(artist)
            print(f"\n {artist} added!")
    time.sleep(0.5)
