import pandas as pd;
import numpy as np;
import scipy as sp;
import sklearn;
import sys;
from nltk.corpus import stopwords;
import nltk;
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

stop_words = stopwords.words('english')
with open('additional_stop_words.asw', 'rb') as filehandle:
    stpwrds_extension = pickle.load(filehandle)
stop_words.extend(stpwrds_extension)

def cleaning(csvname,email,links,specchars,bitricnt,bithresh,trithresh,stpwrds):
    print(int(bitricnt))
    print(int(bithresh))
    print(int(trithresh))
    print("Cleaning...")
    ##Input file
    data = pd.read_csv(csvname, 
    error_bad_lines=False)
    # We only need the Headlines text column from the data
    data_text = data[['data']]
    data_text = data_text.astype('str');
    data = data_text.data.values.tolist()
    ##

    ##Cleaning
    # Remove Emails
    if(email == 1):
        print('email')
        data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
    if(links == 1):
        print('link')
        # Remove new line characters
        data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]

    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
    if(specchars == 1):
        print('chars')
        data_words = list(sent_to_words(data))

    bigram = gensim.models.Phrases(data_words, min_count=int(bitricnt), threshold=int(bithresh)) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=int(trithresh))  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """https://spacy.io/api/annotation"""
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out
    if(stpwrds == 1):
        print('words')
        # Remove Stop Words
        data_words_nostops = remove_stopwords(data_words)
        
    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)

    nlp = spacy.load('en_core_web_sm')

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    ##
    return data_lemmatized

def mkcorpus(data_lemmatized):
    print("Creating corpus")
    ##Creating the corpus
    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    ##
    return corpus

def ldamdl(corpus,data_lemmatized,numtopics,randomstate,update,chunksize,tpasses,wrdpt):
    id2word = corpora.Dictionary(data_lemmatized)
    print(data_lemmatized,numtopics,randomstate,update,chunksize,tpasses)
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                   id2word=id2word,
                                                   num_topics=numtopics, 
                                                   random_state=randomstate,
                                                   update_every=update,
                                                   chunksize=chunksize,
                                                   passes=tpasses,
                                                   alpha='auto',
                                                   per_word_topics=True)
    pprint(lda_model.print_topics(numtopics,wrdpt))
    data = lda_model.print_topics(numtopics,wrdpt)
    doc_lda = lda_model[corpus]
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis, 'LDA_Visualization.html')
    return str(data)
    
def mallda(corpus,data_lemmatized):
    print("Traning..")
    id2word = corpora.Dictionary(data_lemmatized)
    mallet_path = "C:/Users/Asus/Documents/project-thesis/mallet-2.0.8/bin/mallet"
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)
    pprint(ldamallet.show_topics(formatted=False))
    data = ldamallet.show_topics(formatted=False)
    #vis = pyLDAvis.gensim.prepare(ldamallet, corpus, id2word)
    #pyLDAvis.save_html(vis, 'LDA_Visualization.html')
    return str(data)
    
def nmfmdl(data,numtopics,mfeatures,mindf,maxdf):
    num_topics = numtopics
    train_headlines_sentences = [' '.join(text) for text in data]
    vectorizer = CountVectorizer(analyzer='word', max_features=mfeatures,min_df=mindf,max_df=maxdf);
    x_counts = vectorizer.fit_transform(train_headlines_sentences);
    transformer = TfidfTransformer(smooth_idf=False);
    x_tfidf = transformer.fit_transform(x_counts);
    xtfidf_norm = normalize(x_tfidf, norm='l1', axis=1)
    #obtain a NMF model.
    model = NMF(n_components=num_topics, init='nndsvd');
    #fit the model
    model.fit(xtfidf_norm)
    def get_nmf_topics(model, n_top_words):
    
        #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
        feat_names = vectorizer.get_feature_names()
        word_dict = {};
        for i in range(num_topics):
            print("Working on\n")
            #for each topic, obtain the largest values, and add the words they map to into the dictionary.
            words_ids = model.components_[i].argsort()[:-20 - 1:-1]
            words = [feat_names[key] for key in words_ids]
            word_dict['Topic # ' + '{:02d}'.format(i+1)] = words;
            print(word_dict['Topic # ' + '{:02d}'.format(i+1)])
        return pd.DataFrame(word_dict);
    
    def fileout(model, n_top_words):
    
        #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
        feat_names = vectorizer.get_feature_names()

        nmfval = ""
        word_dict = {};
        for i in range(num_topics):
            print("Working on\n")
            #for each topic, obtain the largest values, and add the words they map to into the dictionary.
            words_ids = model.components_[i].argsort()[:-20 - 1:-1]
            words = [feat_names[key] for key in words_ids]
            word_dict['Topic # ' + '{:02d}'.format(i+1)] = words;
            nmfval = nmfval + str(word_dict['Topic # ' + '{:02d}'.format(i+1)])
            print(word_dict['Topic # ' + '{:02d}'.format(i+1)])
        return nmfval;

    dict = fileout(model, num_topics)
    print(dict)
    return str(dict)
