import spacy
import os

folder = os.path.join("WEB", "BOA", "2018U.S.TrustWealth&WorthStudy")
nlp = spacy.load("en_core_web_sm")
doc = nlp(open(os.path.join(folder, "content.txt"), 'r').read())
noun_chunks = list(doc.noun_chunks)
# print(noun_chunks)
# for word in doc:
#     print(word.text, word.lemma_)

for token in doc:
    print(token, token.idx)
# sentences = list(doc.sents)
# print(sentences[1].text)    # 'Peach is the superior emoji.'
