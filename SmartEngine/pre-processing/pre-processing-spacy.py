import os
import sys
import spacy
from spacy import displacy
# this is the core module for english language we may need to load other languages based on the articles.
nlp = spacy.load("en_core_web_sm")
doc = nlp(open(os.path.join(sys.path[0], "sample"), "r").read())
# Change the below from render to serve to get the graph served on a webpage

displacy.render(doc, style="dep")
# create list of sentence tokens, these are just sentences not sure how we would use them for now
sents_list = []
for sent in doc.sents:
    sents_list.append(sent.text)
print(sents_list)
# The following does lemmatization of words to the root word and origin.
for word in doc:
    print(word.text, word.lemma_)

# the below identifies different entitles for example it will classify persons and orgs based on the sentiment
entities = [(i, i.label_, i.label) for i in doc.ents]
print(entities)

# The below does a token heatmap for all the tokens in the article
for token in doc:
    print(token, token.idx)

# The below does a object analysis and defines grammar associated.

for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
