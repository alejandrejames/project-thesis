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
import tkinter as tk
import os
import shutil

def cleaning(csvname,email,links,specchars,stpwrds,dpp_entry_4):
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    stpwrds_extension = ''
    with open('additional_stop_words.asw', 'r') as filehandle:
        string1 = filehandle.read()
        stpwrds_extension = stpwrds_extension+','+string1
    stpwrds_extension = stpwrds_extension.split('\n')
    stop_words.extend(stpwrds_extension)
    #print(stpwrds_extension,'\n')
    stpwrds_extension2 = ''
    with open('additional_stop_words_tagalog.asw', 'r') as filehandle:
        string1 = filehandle.read()
        stpwrds_extension2 = stpwrds_extension2+','+string1
    stpwrds_extension2 = stpwrds_extension2.split('\n')
    stop_words.extend(stpwrds_extension2)
    #print(stpwrds_extension2,'\n')
    stpwrds_extension3 = ''
    with open('additional_stop_words_mallet.asw', 'r') as filehandle:
        string1 = filehandle.read()
        stpwrds_extension3 = stpwrds_extension3+','+string1
    #print(stpwrds_extension,'\n')
    stpwrds_extension3 = stpwrds_extension3.split('\n')
    stop_words.extend(stpwrds_extension3)
    #print(stop_words)
    dpp_entry_4.insert(tk.END,'Stopwords Loaded\n')
    dpp_entry_4.see(tk.END)
    dpp_entry_4.insert(tk.END,'Cleaning...\n')
    dpp_entry_4.see(tk.END)
    ##Input file
    data = pd.read_csv(csvname, 
    error_bad_lines=False)
    # We only need the Headlines text column from the data
    data_text = data[['data']]
    data_text = data_text.astype('str');
    data = data_text.data.values.tolist()
    ##
    shutil.copy2(csvname, 'files/dataset-viewing.csv')
    ##Cleaning
    # Remove Emails
    if(email == 1):
        dpp_entry_4.insert(tk.END,'Removing emails...')
        dpp_entry_4.see(tk.END)
        data = [re.sub('\S*@\S*\s?\_\S_\S.\s.', '', sent) for sent in data]
        data = [re.sub(r'[^\x00-\x7f]',r'', sent) for sent in data]
        data = [re.sub('@[^\s]+','',sent) for sent in data]
        data = [re.sub(r"http\S+", "", sent) for sent in data]
    dpp_entry_4.insert(tk.END,'Success\n')
    
    if(links == 1):
        dpp_entry_4.insert(tk.END,'Removing Links...')
        dpp_entry_4.see(tk.END)
        # Remove new line characters
        data = [re.sub('\s+', ' ', sent) for sent in data]
    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]
    dpp_entry_4.insert(tk.END,'Sucess\n')
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
    if(specchars == 1):
        dpp_entry_4.insert(tk.END,'Removing Special Characters...')
        dpp_entry_4.see(tk.END)
        data_words = list(sent_to_words(data))
    dpp_entry_4.insert(tk.END,'Success\n')
    dpp_entry_4.see(tk.END)
    
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

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
    with open('clean1.txt', 'w') as filehandle:
        line = ' '.join(str(x) for x in data_words)
        filehandle.write(str((line + '\n').encode("utf-8")))
    if(stpwrds == 1):
        dpp_entry_4.insert(tk.END,'Removing Stopwords...')
        dpp_entry_4.see(tk.END)
        # Remove Stop Words
        data_words_nostops = remove_stopwords(data_words)
    dpp_entry_4.insert(tk.END,'Success\n')
    dpp_entry_4.see(tk.END)

    dpp_entry_4.insert(tk.END,'Creating cleaned data set...')
    dpp_entry_4.see(tk.END)
    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)
    with open('clean2.txt', 'w') as filehandle:
        line = ' '.join(str(x) for x in data_words_bigrams)
        filehandle.write(str((line + '\n').encode("utf-8")))

    nlp = spacy.load('en_core_web_sm')
    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    ##
    
    data_lemmatized2 = remove_stopwords(data_lemmatized)
    with open('clean.txt', 'w') as filehandle:
        line = ' '.join(str(x) for x in data_lemmatized2)
        filehandle.write(str((line + '\n').encode("utf-8")))
    with open('clean.txt', 'r') as filehandle:
        string = filehandle.read()
    lista = string.split('] [')
    with open('cleaneddataset-readable.csv', 'w') as filehandle:
        filehandle.write('Cleaned Words')
        filehandle.write('\n')
        for x in lista:
            filehandle.write(x)
            filehandle.write('\n')
    
    dpp_entry_4.insert(tk.END,'Completed\n')
    dpp_entry_4.see(tk.END)
    return data_lemmatized2

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

def ldamdl(corpus,data_lemmatized,numtopics,randomstate,update,tpasses,wrdpt):
    id2word = corpora.Dictionary(data_lemmatized)
    #print(data_lemmatized,numtopics,randomstate,update,chunksize,tpasses)
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                   id2word=id2word,
                                                   num_topics=numtopics,
                                                   update_every=1,
                                                   chunksize=100,
                                                   passes=tpasses,
                                                   alpha='auto',
                                                   per_word_topics=True,iterations=update)
    #pprint(lda_model.print_topics(numtopics,wrdpt))
    data = lda_model.print_topics(numtopics,wrdpt)
    with open('ldamdl.lda', 'wb') as filehandle:
            pickle.dump(str(data),filehandle,protocol=pickle.HIGHEST_PROTOCOL)
    doc_lda = lda_model[corpus]
    #for t in range(lda_model.num_topics):
     #   plt.figure()
      #  plt.imshow(WordCloud().fit_words(dict(lda_model.show_topic(t, 200))))
       # plt.axis("off")
        #plt.title("Topic #" + str(t))
       # plt.show()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis, 'LDA_Visualization.html')
    return str(data)
    
def mallda(corpus,data_lemmatized,numtopics,wpt,iterat):
    print("Traning..")
    id2word = corpora.Dictionary(data_lemmatized)
    mallet_path = os.getcwd()
    mallet_path = mallet_path + "/mallet-2.0.8/bin/mallet"
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=numtopics, id2word=id2word,workers=4, prefix=None,optimize_interval=0, iterations=iterat)
    #pprint(ldamallet.show_topics(formatted=False,num_topics=numtopics, num_words=wpt))
    data = ldamallet.show_topics(formatted=True,num_topics=numtopics, num_words=wpt)
    #print(str(data))
    lda_model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(ldamallet)
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis, 'LDA_Visualization.html')
    with open('ldamdl.lda', 'wb') as filehandle:
            pickle.dump(str(data),filehandle,protocol=pickle.HIGHEST_PROTOCOL)
    return str(data)
    
def nmfmdl(data,numtopics,mfeatures,wpt,iterat,rstate):
    num_topics = numtopics
    train_headlines_sentences = [' '.join(text) for text in data]
    vectorizer = CountVectorizer(analyzer='word', max_features=mfeatures);
    x_counts = vectorizer.fit_transform(train_headlines_sentences);
    transformer = TfidfTransformer(smooth_idf=False);
    x_tfidf = transformer.fit_transform(x_counts);
    xtfidf_norm = normalize(x_tfidf, norm='l1', axis=1)
    #obtain a NMF model.
    model = NMF(n_components=num_topics, init='nndsvd',max_iter=iterat);
    #fit the model
    model.fit(xtfidf_norm)
    def get_nmf_topics(model, n_top_words):
    
        #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
        feat_names = vectorizer.get_feature_names()
        word_dict = {};
        for i in range(num_topics):
            print("Working on\n")
            #for each topic, obtain the largest values, and add the words they map to into the dictionary.
            words_ids = model.components_[i].argsort()[:-n_top_words - 1:-1]
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
            words_ids = model.components_[i].argsort()[:-n_top_words - 1:-1]
            words = [feat_names[key] for key in words_ids]
            word_dict['Topic # ' + '{:02d}'.format(i+1)] = words;
            nmfval = nmfval + str(word_dict['Topic # ' + '{:02d}'.format(i+1)])
            #print(word_dict['Topic # ' + '{:02d}'.format(i+1)])
        return nmfval;
    #dict2 = get_nmf_topics(model, 5)
    dict = fileout(model, wpt)
    #pprint(dict2)
    #print(str(dict))
    with open('nmfmdl.nmf', 'wb') as filehandle:
            pickle.dump(str(dict),filehandle,protocol=pickle.HIGHEST_PROTOCOL)
    #print(dict2)
    #with open('nmf1', 'w') as filehandle:
        #filehandle.write(str(dict2))
    with open('nmf2', 'w') as filehandle:
        filehandle.write(str(dict))
    #print('-------------------------------------------------------')
    #print(dict)
    return str(dict)
