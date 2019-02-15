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

#topics = ['mayon','volcano','eruption','philippine','people','alert_level','ash','good','relief','flee',]
topics = ['evacuate','displace','home','resident','smoke','authority','raise','beautiful','permanent','increase']

def getlbllda(topics):
     with open('files/lbllistlda.lst','r') as filehandle:
          stringfrm = filehandle.readline()
     
     lbllist = stringfrm.split(',')
     num = 0
     labelscores = []
     for x in (lbllist):
          labelscores.append(int(0))
          num = num + 1

     for x in range(0,num):
          score = 0
          labelwrds = []
          with open('files/ldalabel-'+lbllist[x]+'.lbl') as file:
               wrds = file.readline()
               labelwrds = wrds.split(',')
          print('scoring')     
          for y in topics:
               if y in labelwrds:
                   score = score + 1
               else:
                    continue
               print('--',y)
          
          
          labelscores[x] = score
     
     print('------------------------------')
     print(lbllist)
     print(labelscores)
     counter = 0
     maxscore = max(labelscores)
     for x in labelscores:
          if(x==maxscore):
               counter = counter + 1
          else:
               continue
     if(maxscore == 0 or counter > 1):
          tplbl = 'No Label'
     else:
          indexnum = labelscores.index(maxscore)
          tplbl = lbllist[indexnum]

     return tplbl

def getlblnmf(topics):
     with open('files/lbllistnmf.lst','r') as filehandle:
          stringfrm = filehandle.readline()
     
     lbllist = stringfrm.split(',')
     num = 0
     labelscores = []
     for x in (lbllist):
          labelscores.append(int(0))
          num = num + 1

     for x in range(0,num):
          score = 0
          labelwrds = []
          with open('files/nmflabel-'+lbllist[x]+'.lbl') as file:
               wrds = file.readline()
               labelwrds = wrds.split(',')
          print('scoring')     
          for y in topics:
               if y in labelwrds:
                   score = score + 1
               else:
                    continue
               print('--',y)
          
          
          labelscores[x] = score
     
     print('------------------------------')
     print(lbllist)
     print(labelscores)
     counter = 0
     maxscore = max(labelscores)
     for x in labelscores:
          if(x==maxscore):
               counter = counter + 1
          else:
               continue
     if(maxscore == 0 or counter > 1):
          tplbl = 'No Label'
     else:
          indexnum = labelscores.index(maxscore)
          tplbl = lbllist[indexnum]

     return tplbl

print(getlblnmf(topics))
