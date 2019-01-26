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
    label1score = 0;label2score = 0;label3score = 0;label4score = 0;label5score = 0;label6score = 0;label7score = 0;label8score = 0;label9score = 0;label0score = 0;
    tpclabel = []
    for x in topic:
        if(x=='mayon' or x=='volcano' or x =='explode' or x == 'sunday' or x=='abo' or x=='lumikas' or x=='photo' or x =='wait' or x == 'maount' or x=='evacuee'):
            label1score = label1score + 1
        if(x=='safe' or x=='stay' or x =='ensure' or x == 'relative' or x=='pray' or x=='bless' or x=='hope' or x =='ashfall' or x == 'stop' or x=='praying'):
            label2score = label2score + 1
        if(x=='city' or x=='photo' or x =='boulevard' or x == 'village' or x=='rise' or x=='hossi' or x=='pray' or x =='onslaught' or x == 'augmentation' or x=='municipality'):
            label3score = label3score + 1
        if(x=='philippine' or x=='volcano' or x =='thought' or x == 'sunrise' or x=='evacuate' or x=='sunday' or x=='threat' or x =='experience' or x == 'relief_effort' or x=='local_partner'):
            label4score = label4score + 1
        if(x=='family' or x=='affect' or x =='outreach' or x == 'friend' or x=='day' or x=='reminder' or x=='close' or x =='home' or x == 'area' or x=='vision'):
            label5score = label5score + 1
        if(x=='lava' or x=='ash' or x =='abo' or x == 'flow' or x=='fountaining' or x=='ulat' or x=='umaga' or x =='usok' or x == 'glow' or x=='spew'):
            label6score = label6score + 1
        if(x=='level' or x=='tomorrow' or x =='suspend' or x == 'class' or x=='private' or x=='public' or x=='downgrade' or x =='province' or x == 'raise' or x=='major'):
            label7score = label7score + 1
        if(x=='people' or x=='evacuate' or x =='volcano' or x == 'home' or x=='pray' or x=='die' or x=='mount' or x =='beautiful' or x == 'threat' or x=='relief_effort'):
            label8score = label8score + 1
        if(x=='eruption' or x=='volcano' or x =='beautiful' or x == 'day' or x=='hazardous' or x=='imminent' or x=='hour' or x =='warn' or x == 'volcanic' or x=='kababayan'):
            label9score = label9score + 1
        if(x=='sale_period' or x=='province' or x =='beautiful' or x == 'ash' or x=='disaster' or x=='dangerous' or x=='bless' or x =='aurora' or x == 'evacuee' or x=='plume'):
            label0score = label0score + 1
    highest = max(label1score,label2score,label3score,label4score,label5score,label6score,label7score,label8score,label9score,label0score)
    #print(highest,'\n')
    #print(label1score,label2score,label3score,label4score,label5score)
    if(highest == 0):
        tpclabel.append('No Label')
    if(highest == label1score):
        tpclabel.append('evacuate')
    if(highest == label2score):
        tpclabel.append('pray')
    if(highest == label3score):
        tpclabel.append('augment')
    if(highest == label4score):
        tpclabel.append('experience')
    if(highest == label5score):
        tpclabel.append('outreach')
    if(highest == label6score):
        tpclabel.append('lavaflow')
    if(highest == label7score):
        tpclabel.append('suspension')
    if(highest == label8score):
        tpclabel.append('dangerous')
    if(highest == label9score):
        tpclabel.append('prone')
    if(highest == label0score):
        tpclabel.append('sunrise')
    #print(tpclabel)

    return(tpclabel)

def getlbllda(topic):
    label1score = 0;label2score = 0;label3score = 0;label4score = 0;label5score = 0;label6score = 0;label7score = 0;label8score = 0;label9score = 0;label0score = 0;
    tpclabel = []
    #print(topic,'\n\n')
    for x in topic:
        if(x=='conduct' or x=='food' or x =='chapter' or x == 'aid' or x=='remain' or x=='expect' or x=='effect' or x =='plan' or x == 'force' or x=='service'):
            label1score = label1score + 1
        if(x=='activity' or x=='today' or x =='detail' or x == 'contact' or x=='tendency' or x=='volunteer' or x=='federation' or x =='danger' or x == 'enter' or x=='column'):
            label2score = label2score + 1
        if(x=='relief' or x=='evacuation' or x =='displace' or x == 'provide' or x=='school' or x=='distribute' or x=='tourist' or x =='increase' or x == 'mask' or x=='majestic'):
            label3score = label3score + 1
        if(x=='resident' or x=='include' or x =='province' or x == 'school' or x=='distribute' or x=='tourist' or x=='increase' or x =='mask' or x == 'north' or x=='majestic'):
            label4score = label4score + 1
        if(x=='people' or x=='family' or x =='evacuate' or x == 'donation' or x=='affect' or x=='home' or x=='permanent' or x =='student' or x == 'thousand' or x=='benificiary'):
            label5score = label5score + 1
        if(x=='alert_level' or x=='good' or x =='local' or x == 'authority' or x=='raise' or x=='beautiful' or x=='work' or x =='fascinating' or x == 'menacing' or x=='collectively'):
            label6score = label6score + 1
        if(x=='volcano' or x=='philippine' or x =='stay' or x == 'city' or x=='support' or x=='week' or x=='live' or x =='active' or x == 'alert' or x=='mount'):
            label7score = label7score + 1
        if(x=='mayon' or x=='eruption' or x =='continue' or x == 'kababayan' or x=='sunday' or x=='visit' or x=='recent' or x =='naitala' or x == 'nature' or x=='posible' or x=='possible'):
            label8score = label8score + 1
        if(x=='lava' or x=='safe' or x =='flow' or x == 'flee' or x=='photo' or x=='danger_zone' or x=='area' or x =='reach' or x == 'smoke' or x=='video'):
            label9score = label9score + 1
        if(x=='ash' or x=='time' or x =='volcanic' or x == 'spew' or x=='sign' or x=='summit' or x=='slope' or x =='warn' or x == 'hour' or x=='continuosly'):
            label0score = label0score + 1
    highest = max(label1score,label2score,label3score,label4score,label5score,label6score,label7score,label8score,label9score,label0score)
    #print(highest,'\n')
    #print(label1score,label2score,label3score,label4score,label5score)
    if(highest == 0):
        tpclabel.append('No Label')
    if(highest == label1score):
        tpclabel.append('support')
    if(highest == label2score):
        tpclabel.append('volunteers')
    if(highest == label3score):
        tpclabel.append('lavaflow')
    if(highest == label4score):
        tpclabel.append('mask')
    if(highest == label5score):
        tpclabel.append('beneficiaries')
    if(highest == label6score):
        tpclabel.append('linkages')
    if(highest == label7score):
        tpclabel.append('alert')
    if(highest == label8score):
        tpclabel.append('record')
    if(highest == label9score):
        tpclabel.append('evacuate')
    if(highest == label0score):
        tpclabel.append('lavaflow')
    print(tpclabel)

    return(tpclabel)

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
