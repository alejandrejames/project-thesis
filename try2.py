import pandas as pd;
import numpy as np;
import scipy as sp;
import sklearn;
import sys;
from nltk.corpus import stopwords;
import nltk;
import gensim
from gensim.models import ldamodel
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import gensim.corpora;
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer;
from sklearn.decomposition import NMF;
from sklearn.preprocessing import normalize;
import pickle;
import re;
from pprint import pprint
import spacy
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import webbrowser
from time import sleep
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS
from gensim.models import CoherenceModel

with open('cleaneddata.cds', 'rb') as filehandle:
    data_lemmatized = pickle.load(filehandle)
# Create Corpus
texts = data_lemmatized
id2word = corpora.Dictionary(data_lemmatized)
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]
#print(data_lemmatized,numtopics,randomstate,update,chunksize,tpasses)
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                   id2word=id2word,
                                                   num_topics=20, 
                                                   random_state=100,
                                                   update_every=40000,
                                                   chunksize=100,
                                                   passes=10,
                                                   alpha='auto',
                                                   per_word_topics=True)
#pprint(lda_model.print_topics(numtopics,wrdpt))
model = gensim.models.wrappers.LdaMallet('C:/Users/Asus/Documents/project-thesis/mallet-2.0.8/bin/mallet', corpus=corpus, num_topics=10, id2word=id2word,workers=4, prefix=None,optimize_interval=0, iterations=1000)
print(model.show_topics(formatted=False,num_topics=10, num_words=10))
data = lda_model.print_topics(20,10)
with open('ldamdl.lda', 'wb') as filehandle:
    pickle.dump(str(data),filehandle,protocol=pickle.HIGHEST_PROTOCOL)
doc_lda = lda_model[corpus]
#for t in range(lda_model.num_topics):
    #plt.figure()
    #plt.imshow(WordCloud().fit_words(dict(lda_model.show_topic(t, 200))))
    #plt.axis("off")
    #plt.title("Topic #" + str(t))
    # plt.show()
def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet('C:/Users/Asus/Documents/project-thesis/mallet-2.0.8/bin/mallet', corpus=corpus, num_topics=num_topics, id2word=id2word)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='u_mass')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values
model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=2, limit=10, step=1)
limit=10; start=2; step=1;
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.show()
for m, cv in zip(x, coherence_values):
    print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
