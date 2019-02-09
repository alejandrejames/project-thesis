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
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

with open('files/lbllistlda.lst','r') as filehandle:
     stringfrm = filehandle.readline()

lbllist = stringfrm.split(',')

labelwrds = []
num = 0
for x in lbllist:
     words = []
     with open('files/ldalabel-'+x+'.lbl') as filehandle:
          sentence = filehandle.readline()
          words = sentence.split()
     labelwrds.append(words)
     num = num + 1

labellistscores = []
for y in range(0,num):
     labellistscores.append(int(0))

topic = ['relief','evacuation','displace','provide','alert_level','good','local','authority','raise','beautiful','work',]
for x in topic:
     for y in range(0,num):
          if(x in labelwrds[y]):
               labellistscores[y] = labellistscores[y] + 1


