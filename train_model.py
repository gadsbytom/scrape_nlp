"""This file rebalances classes as necessary, vectorizes the language, and trains the Naive Bayes algorithm"""

import time
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from imblearn.over_sampling import SMOTE
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def train_my_nb(X, y):
    """update the Naive Bayes model"""
    m = MultinomialNB()
    m.fit(X, y)
    time.sleep(1)
    print("\n ------------------------------------------------------------")
    print(" Model is trained")
    time.sleep(0.5)
    return m


def rebalance_my_datasets(X, y):
    """bootstrap all minority classes with less than 4 data points up to 6, else SMOTE doesn't work"""
    # only resample for n_classes > 1
    if len(set(y)) > 1:
        values, counts = np.unique(y, return_counts=True)
        small_classes = [x[0] for x in list(zip(values, counts)) if x[1] < 4]
        extra_x = [X]
        extra_y = [y]
        for c in small_classes:
            upsample_index = np.where(y == c)[0]
            extra_x.append(X[upsample_index])
            extra_y.append(y[upsample_index])

        extra_x = tuple([x.todense() for x in extra_x])
        X = np.concatenate(extra_x, axis=0)
        y = np.concatenate(extra_y, axis=0)
        sm = SMOTE(sampling_strategy="auto")
        return sm.fit_resample(X, y)
    else:
        return X, y


def tfidf(x):
    """convert all items to bag of words"""
    all_lyrics = []
    artist_name = []
    path = "./songs/"
    for artist in x:
        folder = os.path.join(path, artist, "")
        for file in os.listdir(folder):
            if artist in file and ".txt" in file:
                with open(folder + file, "r") as f:
                    all_lyrics.append(f.read())
                    artist_name.append(artist)
        if all_lyrics:
            save_word_cloud(all_lyrics, folder, artist)
    artist_name = pd.factorize(artist_name)[0]
    tv = TfidfVectorizer()
    vec_lyrics = tv.fit_transform(all_lyrics)
    time.sleep(1)
    print("\n ------------------------------------------------------------")
    print(" Song lyrics vectorised")
    return vec_lyrics, artist_name, tv
