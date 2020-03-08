"""This file carries out the naive bayes prediction"""

import time
from sklearn.naive_bayes import MultinomialNB

def train_my_nb(X,y):
    """update the Naive Bayes model"""
    m = MultinomialNB()
    m.fit(X,y)
    time.sleep(1)
    print("\n ------------------------------------------------------------")
    print(' Model is trained')
    time.sleep(1)
    return m
