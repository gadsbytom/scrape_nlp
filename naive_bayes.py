import time
from sklearn.naive_bayes import MultinomialNB

def train_my_nb(x,y):
    m = MultinomialNB()
    m.fit(x,y)
    return m
