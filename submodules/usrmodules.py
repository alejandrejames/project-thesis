import subprocess
import os
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
import pickle

def collectdata(query,num,startd,endd,flname):
    collect = 'python Exporter.py --querysearch "'
    collect = collect + query
    collect = collect + '" --since '+startd+' --until '+endd+' --maxtweets '+num+' --output '+flname+'.csv'
    print(collect)
    subprocess.call(collect, shell=True)

def getlblnmf(topic):
    label1score = 1;label2score = 3;label3score = 4;label4score = 8;label5score = 2;
    tpclabel = []
    for x in topic:
        if(x=='word1' or x=='word2' or x =='word3' or x == 'word4'):
            label1score = label1score + 1
        if(x == 'word1' or x == 'word2' or x == 'word3' or x == 'word4'):
            label2score = label2score + 1
        if(x == 'word1' or x == 'word2' or x == 'word3' or x == 'word4'):
            label3score = label3score + 1
        if(x == 'word1' or x == 'word2' or x == 'word3' or x == 'word4'):
            label4score = label4score + 1
        if(x == 'word1' or x == 'word2' or x == 'word3' or x == 'word4'):
            label5score = label5score + 1
    highest = max(label1score,label2score,label3score,label4score,label5score)
    if(highest == 0):
        tpclabel.append('No Label')
        print('tpclabel')
    if(highest == label1score):
        tpclabel.append('label1')
    if(highest == label2score):
        tpclabel.append('label1')
    if(highest == label3score):
        tpclabel.append('label1')
    if(highest == label4score):
        tpclabel.append('label1')
    if(highest == label5score):
        tpclabel.append('label1')
    print(tpclabel)

def ldaout(fl4):
    fl3 = open('ldaresult.res','r')
    conts = fl3.readline()
    flag=0
    num = 0
    for x in conts:
        if(x=='('):
            tagstr = '<tr><td>Topic'+str(num)+'</td><td>'
            fl4.write(tagstr)
        elif(x==')'):
            fl4.write('</td></tr>')
            num = int(num) + 1
        elif(x=='*'):
            fl4.write('-')
        elif(x=='+'):
            fl4.write(',')
        elif(x==','):
            q = 0
        elif(x=='"'):
            q = 0
        elif(x=='['):
            q = 0
        elif(x==']'):
            q = 0
        elif(x=="'"):
            q = 0
        else:
            fl4.write(x)
    fl3.close()

def nmfout(fl2):
    fl = open('nmfresult.res','r')
    conts = fl.readline()
    flag=0
    num = 0
    topicsg = []
    topicwrd = []
    for x in conts:
        if(x=='['):
            tagstr = '<tr><td>Topic'+str(num)+'</td><td>'
            fl2.write(tagstr)
        elif(x==']'):
            fl2.write('</td></tr>')
            num = int(num) + 1
            #print(topicsg)
            getlblnmf(topicsg)
            topicsg = []
        elif(x=="'"):
            q = 0
            charstr = ''.join(topicwrd)
            #print(charstr)
            topicsg.append(charstr)
            topicwrd = [] 
        else:
            fl2.write(x)
            topicwrd.append(x)
    fl.close()

def ldafreqbar():
    with open('ldamdl.lda', 'rb') as filehandle:
        lda_model = pickle.load(filehandle)
    stringfrm = ""
    thelist = []
    for x in lda_model:
        if(x == '+'):
            thelist.append(stringfrm)
            #print(stringfrm)
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

def nmffreqbar():
    with open('nmfmdl.nmf', 'rb') as filehandle:
        lda_model = pickle.load(filehandle)
    stringfrm = ""
    thelist = []
    for x in lda_model:
        if(x == ','):
            thelist.append(stringfrm)
            #print(stringfrm)
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
    print(thelist)
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
