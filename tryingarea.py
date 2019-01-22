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
with open('ldamdl.lda', 'rb') as filehandle:
     lda_model = pickle.load(filehandle)
#print(lda_model)
num = 0
title = 'model'
wordcloud = WordCloud(
        background_color='white',
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ,width=800,height=400).generate(str(lda_model))
fig = plt.figure(1, figsize=(20, 10))
plt.axis('off')

stringfrm = ""
thelist = []
for x in lda_model:
     if(x == '+'):
          thelist.append(stringfrm)
          print(stringfrm)
          stringfrm = ""
     elif(x == '\''):
          continue
     elif(x == '['):
          continue
     elif(x == '('):
          continue
     elif(x == ')'):
          continue
     elif(x == '*'):
          continue
     elif(x == '-'):
          continue
     elif(x == ' '):
          continue
     elif(x == ']'):
          continue
     elif(x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == '0'):
          continue
     elif(x == '.'):
          continue
     elif(x == '"'):
          continue
     else:
          stringfrm = stringfrm + x

thelist2 = []
thelist3 = []
print(len(thelist))
for x in range(0,len(thelist)):
     num = 0
     if(thelist[x] in thelist2):
          continue
     else:
          for y in range(0,len(thelist)):
               if(thelist[x]==thelist[y]):
                    num = num + 1
               else:
                    continue
          #print("Word=",thelist[x],"Occur=",num)
          thelist2.append(thelist[x])
          thelist3.append(num)
          
objects = thelist2
y_pos = np.arange(len(thelist2))
performance = thelist3
plt.figure(1, figsize=(20, 10))
plt.axis('on')
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects,rotation='vertical',fontsize=10)
plt.ylabel('Frequency')
plt.title('Words')
plt.savefig('bar', dpi=350)
plt.show()


plt.imshow(wordcloud)
plt.savefig('ldawc')
plt.show()

