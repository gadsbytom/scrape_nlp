"""This is the primary file for handling new song inputs"""

import time
import os
import re
import pandas as pd
import sys
from pyfiglet import Figlet
from tqdm import tqdm
import numpy as np
from scrape_songs_with_bs4 import compile_artists, grab_artist_lyrics
from vectorize_songs_with_tfidf import tfidf
from train_naive_bayes import train_my_nb, rebalance_my_datasets


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
    banner = Figlet()
    render_welcome(banner)

    #scrape all intputted artists and train the model
    artist_links, artist_names = compile_artists(banner)
    clean_artists = grab_artist_lyrics(artist_links, artist_names, banner)
    lyrics, names, tv = tfidf(clean_artists)
    lyrics, names = rebalance_my_datasets(lyrics,names)
    model = train_my_nb(lyrics,names)

    #guess  the artist from unseen text
    guess = input(f"\n Now paste in a song lyric from one of your artists to see if the model works:\n\n ")
    prediction = guess_artist(guess, tv, model)
    print(banner.renderText(clean_artists[prediction.argmax()]))
