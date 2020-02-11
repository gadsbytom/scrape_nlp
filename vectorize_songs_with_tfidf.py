"""This file converts strings to BOW vectors"""

import time
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def bag_of_words(y):
    """convert all items to bag of words"""
    all_lyrics = []
    artist_name = []
    path = './songs/'
    for artist in y:
        for file in os.listdir(path):
            if artist in file and '.txt' in file:
                with open(path + file, 'r') as f:
                    all_lyrics.append(f.read())
                    artist_name.append(artist)

    artist_name = pd.factorize(artist_name)[0]
    tv = TfidfVectorizer()
    vec_lyrics = tv.fit_transform(all_lyrics)
    time.sleep(1)
    print("\n ------------------------------------------------------------")
    print(' Song lyrics vectorised')
    return vec_lyrics, artist_name, tv