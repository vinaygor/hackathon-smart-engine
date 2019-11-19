## **Hackathon Team 6**

An attempt to find the content gaps between the articles published on various websites which falls under financial domain.

##### Details:
This project is divided into four separate modules:

1. ###### Web Scraping
2. ###### Pre-processing
3. ###### Topic Modelling

Let's learn about them in details below:

### 1. Web Scraping

For this hackathon we have scrapped different websites to fetch the content of the articles published. Each of these websites have a different structure on how the content is displayed. Based on the different DOM patterns, we have segregated scraping scripts for each of these websites and can be found under `scraping` folder.

Run command example: `python msimInsight.py`

This will create a `/WEB/MSIM` folder, which will contain the content of all the insight files where the name of the file is a normalized insight URL address.

### 2. Pre-processing

Once we have content data from all the insight articles, we are using `spaCy` [https://spacy.io/] library for:

i. lemmatization of words to the root word and origin

ii. identifying Entities (classification based on sentiment)

iii. creating tokens

iv. generating token heatmap

v.  object analysis and defining grammar

Code for this can be found under `pre-processing` folder.

### 3. Topic Modelling

For topic modelling we are leveraging `gensim` [https://radimrehurek.com/gensim/] library which can help for analyzing plain-text documents for semantic structure. We are using gensim for:

i. lemmatize

ii. stop words removal

iii. training a LDA model and then save the model which can we used for running on a new article

iv. generating a corpus for each of the insight article and creating a dictionary (union) of all the corpus

v. converting documents into vectors using bag-of-words representation
