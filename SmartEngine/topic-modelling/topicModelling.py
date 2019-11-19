import glob
from datetime import datetime
import spacy
import pprint
from nltk.util import ngrams
from gensim import corpora
from gensim import models

import logging
log_file_name = datetime.now().strftime('log/topic_modelling_%Y-%m-%d_%H-%M-%S.log')
logging.basicConfig(filename=log_file_name, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

nlp_en = spacy.load('en_core_web_sm')


def preprocess_text(doc1):
    doc = nlp_en(doc1)
    print("Doc - Orig:", doc)
    # for token in doc:
    #    print(token.text, token.is_stop, token.lemma_)

    # Lemmatize
    doc = [token.lemma_.lower() for token in doc if token.lemma_ != "-PRON-"]
    doc = u' '.join(doc)
    doc = nlp_en.make_doc(doc)
    print("Doc - Lemmatized:", doc)

    # Remove Stop Words
    doc = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
    print("Doc - Removed Stop words:", doc)

    #    bigram = list(ngrams(doc, 2))
    #    print("bigram:", bigram)
    #    trigram = list(ngrams(doc, 3))
    #    print("\ntrigram:", trigram)

    return doc

def train_lda_model():
    path = "data/im/*"

    num_topics = 10
    chunksize = 200
    passes = 20
    iterations = 40
    num_words = topn = 3
    dict_no_below = "not added"
    dict_no_above = "not added"

    content = []
    files = glob.glob(path)
    #print("files list:", files)
    for file in files:
        f = open(file, "r")
        content.append(f.read())
    #print(content)

    corpus = []
    for doc in content:
        corpus.append(preprocess_text(doc))

    dictionary = corpora.Dictionary(corpus)
    #dictionary.filter_extremes(no_below=dict_no_below, no_above=dict_no_above)

    dictionary_file_name = datetime.now().strftime('output/dictionary_%Y-%m-%d_%H-%M-%S.txt')
    dictionary_file = open(dictionary_file_name, "w")
    dictionary_file.write(str(datetime.now())+"\n")
    dictionary_file.write(str(dictionary)+"\n")
    pprint.pprint(dictionary.token2id,dictionary_file)
    dictionary_file.write("\n\nCorpus:"+str(corpus))
    dictionary_file.write("\n\nfiles list:\n")
    pprint.pprint(files, dictionary_file)

    vect = [dictionary.doc2bow(doc) for doc in corpus]
    #print("vector:")
    #pprint.pprint(vect)

    lda_model = models.ldamodel.LdaModel(corpus=vect,
                                         id2word=dictionary,
                                         num_topics=num_topics,
                                         chunksize=chunksize,
                                         passes=passes,
                                         iterations=iterations,
                                         eval_every=1,
                                         alpha='auto',
                                         eta='auto')
    model_file_name = datetime.now().strftime('model/lda_model_msim_test_%Y-%m-%d_%H-%M-%S.txt')
    lda_model.save(model_file_name)

    topic_file_name =  datetime.now().strftime('output/topics_from_model_%Y-%m-%d_%H-%M-%S.txt')
    topic_file = open(topic_file_name, "w")
    topic_file.write(str(datetime.now()))
    topic_file.write("\nTopics from the trained LDA Model:"+model_file_name+".")
    topic_file.write("\nDictionary File Name:" + dictionary_file_name + ".")
    topic_file.write("\n\nnum_topics:"+str(num_topics)+"\n"+"chunksize:"+str(chunksize)+"\n"+"passes:"+str(passes)+"\n"+"iterations:"+str(iterations)+"\n"+"num_words:"+str(num_words)+"\n"+"dict_no_below:"+str(dict_no_below)+"\n"+"dict_no_above:"+str(dict_no_above)+"\n\n")
    pprint.pprint(lda_model.print_topics(num_words=num_words), topic_file)
    topic_file.write("\nTopics with coherence:\n")
    pprint.pprint(lda_model.top_topics(corpus=vect, topn=topn), topic_file)

def run_lda_model():
    path = "data/msim_test/*"
    model_file_name = "model/lda_model_msim_test_2019-11-19_02-17-40.txt"
    model = models.ldamodel.LdaModel.load(model_file_name, mmap='r')

    result_file_name = datetime.now().strftime('output/documents_topic_file_%Y-%m-%d_%H-%M-%S.txt')
    result_file = open(result_file_name, "w")


    result_file.write(str(datetime.now()))
    result_file.write("\nDocument-Topic Mapping from the LDA Model:"+model_file_name+".\n")
    result_file.write("\nDocument Path:")
    result_file.write(path)
    result_file.write("\n\n")

    files = glob.glob(path)
    #print("files list:", files)
    for file in files:
        content = []
        f = open(file, "r")
        content.append(f.read())
        #print(content)

        corpus = []
        for doc in content:
            corpus.append(preprocess_text(doc))
        #print("run_lda_model:Corpus:", corpus)

        dictionary = corpora.Dictionary(corpus)
        #print(dictionary)
        #print("run_lda_model:Dictionary:")

        #pprint.pprint(dictionary.token2id)
        vect = [dictionary.doc2bow(doc) for doc in corpus]
        #print("run_lda_model:vector:")
        #pprint.pprint(vect)

        doc_topics = model.get_document_topics(vect)
        for topic in doc_topics:
            #print(file, ":", topic)
            result_file.write(file)
            result_file.write(":")
            result_file.writelines(str(topic))
            result_file.write("\n")


train_lda_model()
#run_lda_model() n
