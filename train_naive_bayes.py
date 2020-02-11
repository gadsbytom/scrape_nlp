"""This file carries out the naive bayes prediction"""

import time
from sklearn.naive_bayes import MultinomialNB

def train_my_nb(x,y):
    """update the Naive Bayes model"""
    m = MultinomialNB()
    m.fit(x,y)
    time.sleep(1)
    print("\n ------------------------------------------------------------")
    print(' Model is trained')
    return m
