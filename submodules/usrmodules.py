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
from tkinter import *
from tkinter import ttk
import tkinter as tk

def collectdata(query,num,startd,endd,flname):
    collect = 'python Exporter.py --querysearch "'
    collect = collect + query
    collect = collect + '" --since '+startd+' --until '+endd+' --maxtweets '+num+' --output '+flname+'.csv'
    subprocess.call(collect, shell=True)

def getlblnmf(topics,status):
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
        #print('scoring')     
        for y in topics:
            if y in labelwrds:
                score = score + 1
            else:
                continue
            #print('--',y)
          
          
        labelscores[x] = score
     
    #print('------------------------------')
    #print(lbllist)
    #print(labelscores)
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

def getlbllda(topics,status):
    with open('files/lbllistldamal.lst','r') as filehandle:
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
        with open('files/malldalabel-'+lbllist[x]+'.lbl') as file:
            wrds = file.readline()
            labelwrds = wrds.split(',')
        #print('scoring')     
        for y in topics:
            if y in labelwrds:
                score = score + 1
            else:
                continue
            #print('--',y)
          
          
        labelscores[x] = score
     
    #print('------------------------------')
    #print(lbllist)
    #print(labelscores)
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

def getlblldamal(topics,status):
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
        #print('scoring')     
        for y in topics:
            if y in labelwrds:
                score = score + 1
            else:
                continue
            #print('--',y)
          
          
        labelscores[x] = score
     
    #print('------------------------------')
    #print(lbllist)
    #print(labelscores)
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
            #getlblnmf(topicsg)
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
    #print(lda_model.strip('+'))
    for x in lda_model:
        if(x == '*'):
            thelist.append(stringfrm)
            #print(stringfrm)
            stringfrm = ""
        elif(x == "'"):
              continue
        elif(x == '['):
            continue
        elif(x == '('):
            continue
        elif(x == ')'):
            continue
        elif(x == '+'):
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
        elif(x== ','):
            continue
        else:
            stringfrm = stringfrm + x

    thelist.append(stringfrm)
    thelist2 = []
    thelist3 = []
    for x in thelist:
        num = 0
        if(x in thelist2):
            continue
        else:
            for y in thelist:
                if(x==y):
                    num = num + 1
                else:
                    continue
            #print("Word=",thelist[x],"Occur=",num)
            thelist2.append(x)
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
    #print(lda_model)
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
            thelist.append(stringfrm)
            #print(stringfrm)
            stringfrm = ""
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
    for x in thelist:
        #print(x)
        num = 0
        if(x in thelist2):
            continue
        else:
            for y in thelist:
                if(x==y):
                    num = num + 1
                else:
                    continue
            #print("Word=",thelist[x],"Occur=",num)
            thelist2.append(x)
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

class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
