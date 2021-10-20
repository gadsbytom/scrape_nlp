## Scrape and Predict Song Lyrics:
---
### Description:
#### A web scraping and NLP project. The project goals are as follows:

* For a given list of artists, scrape the lyrics from their songs from the internet using Beautiful soup.

* Vectorize their songs using a TfidfVectorizer Bag Of Words model, then train a Naive Bayes classifier on this labelled vector set.

* Allow a user to input some lyrics of their choice, and allow them to see what artist the model thinks the lyrics belong to.
---
### Resources:

#### `predict_artist.py:`
**This is the main entry point for the code**
*This file should be run from the terminal. This file will call all the other files in the collection
**Input: None**
**Output: An artist prediction and prediction probability distribution**

#### `download_songs.py:`
*This module scrapes songs from 'www.metrolyrics.com' using beautiful soup, and saves each song to disk in an appropriately named .txt file inside a 'songs' folder*
**Input: A collection of artists' names**
**Output: A collection of .txt files saved to disk**

#### `train_model.py:`
*This module takes in the tfidf vectors and the labels of the associated artist, and returns a trained naive bayes model*
**Input:  A collection of word vectors, and an associated collection of labels**
**Output: A prediction probability distribution, with order matching the artist collection.**

---
### How to Use:

* Install the file requirements using the python dependencies listed herein:
* Clone the repository here
* Run `python predict_artist.py` from the Terminal
