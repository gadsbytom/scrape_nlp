"""This file carries out the naive bayes prediction"""

import time
from sklearn.naive_bayes import MultinomialNB

def train_my_nb(x,y):
    """update the Naive Bayes model"""
    m = MultinomialNB()
    m.fit(x,y)
    return m
