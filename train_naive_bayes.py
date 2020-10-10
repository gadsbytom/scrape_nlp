"""This file rebalances classes as necessary, then carries out the naive bayes prediction"""

import time
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from imblearn.over_sampling import SMOTE
import pandas as pd

def train_my_nb(X,y):
    """update the Naive Bayes model"""
    m = MultinomialNB()
    m.fit(X,y)  
    time.sleep(1)
    print("\n ------------------------------------------------------------")
    print(' Model is trained')
    time.sleep(1)
    return m


def rebalance_my_datasets(X,y):
    """bootstrap all minority classes with less than 4 data points up to 6, else SMOTE doesn't work"""
    values, counts = np.unique(y, return_counts=True)
    small_classes = [x[0] for x in list(zip(values, counts)) if x[1] <=3]
    extra_x = [X]
    extra_y = [y]
    for c in small_classes:
        upsample_index = np.where(y==c)[0]
        extra_x.append(X[upsample_index])
        extra_y.append(y[upsample_index])

    extra_x = tuple([x.todense() for x in extra_x])
    X = np.concatenate(extra_x, axis=0)
    y = np.concatenate(extra_y,axis=0)
    sm = SMOTE(sampling_strategy='auto')
    X, y = sm.fit_resample(X, y)
    return X,y