"""This is the primary file for handling new song inputs"""


import time
import os
import re
import pandas as pd
import sys
from pyfiglet import Figlet
from tqdm import tqdm
import numpy as np
from scrape_songs_with_bs4 import grab_artist_lyrics
from vectorize_songs_with_tfidf import bag_of_words
from train_naive_bayes import train_my_nb


def render_welcome(banner):
    """CLI visuals for the start of the program"""
    print(banner.renderText('GUESS THE ARTIST!!\n'))
    time.sleep(1)
    print(" This program will scrape songs for as many artists as you like!\n -----------------------------------------------------------")
    time.sleep(1)
    print(" Then train a Naive Bayes model to recognise their lyrics!\n -----------------------------------------------------------")
    time.sleep(1)
    print(" Then you can test how well it has learnt the artists' lyrics!\n -----------------------------------------------------------\n")
    time.sleep(1)

def input_artists():
    """user inputs all artists to be scraped, returns those artists"""
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
    """accepts unseen text and returns a probability distribution"""
    clean_guess = re.sub('[\n\-\?\.\,\(\)]', ' ', guess)
    clean_guess = re.sub('[\']', '', clean_guess)
    clean_guess = [clean_guess]
    vec_guess = tv.transform(clean_guess)
    prediction = model.predict_proba(vec_guess)
    print("\n ------------------------------------------------------------")
    print('\n This looks like a song from:')
    return prediction

if __name__ == '__main__':
    #introductory visuals
    banner = Figlet(font='slant')
    render_welcome(banner)

    #scrape all intputted artists and train the model
    all_artists = input_artists()
    clean_artists = grab_artist_lyrics(all_artists)
    lyrics, names, tv = bag_of_words(clean_artists)
    model = train_my_nb(lyrics,names)

    #guess  the artist from unseen text
    guess = input(f"\n Now paste in a song lyric from one of your artists to see if the model works:\n ")
    prediction = guess_artist(guess, tv, model)
    print(banner.renderText(clean_artists[prediction.argmax()]))
    df = pd.DataFrame(prediction.round(2), columns = all_artists)
    time.sleep(1)
    print("\n ------------------------------------------------------------")
    print(' And the certainty of the guess is:')
    print(df)
