## Scrape and Predict Song Lyrics:
---
### Description:
#### This is a web scraping and NLP project built in Python. The purpose of the code is three-fold:

* For a given list of artists, scrape the lyrics from their songs from the internet.

* Vectorize their songs using a TfidfVectorizer Bag Of Words model, then train a Naive Bayes classifier on this labelled vector set.

* Allow a user to input some lyrics of their choice, and allow them to see what artist the model thinks the lyrics belong to.
---
### Resources:

#### song_predictor.py:
**This is the main entry point for the code**
*This file should be run from the terminal. This file will call all the other files in the collection
**Input: None**
**Output: An artist prediction and prediction probability distribution**

#### soup_scraper.py:
*This module scrapes songs from 'www.metrolyrics.com' using beautiful soup, and saves each song to disk in an appropriately named .txt file*
**Input: A collection of artists' names**
**Output: A collection of .txt files saved to disk**

#### bow.py:
*This module takes the files which have been saved to disk and converts them into tfidf vectors, where the term frequency is scaled by the uniqueness of the results*
**Input: A collection of artists' names**
**Output: A collection of word vectors, an associated collection of labels, and a trained tfidfvectorizer model**

#### naive_bayes.py:
*This module takes in the tfidf vectors and the labels of the associated artist, and returns a trained naive bayes model*
**Input:  A collection of word vectors, and an associated collection of labels**
**Output: A prediction probability distribution, with order matching the artist collection.**

---
### How to Use:

* Install the file requirements using the python dependencies listed herein:
* Clone the repository here
* Run `python song_predictor.py` from the Terminal
