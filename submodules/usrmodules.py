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
    subprocess.call(collect, shell=True)

def getlblnmf(topic,status):
    label1lst = ['mayon','volcano','explode','sunday','abo','lumikas','photo','wait','mount','evacuee']#evacuate
    label2lst = ['safe','stay','ensure','relative','pray','bless','hope','ashfall','stop','praying']#pray
    label3lst = ['city','photo','boulevard','village','rise','hossi','pray','onslaught','augmentation','municipality']#augment
    label4lst = ['philippine','volcano','thought','sunrise','evacuate','sunday','threat','experience','relief_effort','local_partner']#experience
    label5lst = ['family','affect','outreach','friend','day','reminder','close','home','area','vision']#outreach
    label6lst = ['lava','ash','abo','flow','fountaining','ulat','umaga','usok','glow','spew']#lavaflow
    label7lst = ['level','tomorrow','suspend','class','private','public','downgrade','province','raise','major']#suspension
    label8lst = ['people','evacuate','volcano','home','pray','die','mount','beautiful','threat','relief_effort']#dangerous
    label9lst = ['eruption','volcano','beautiful','day','hazardous','imminent','hour','warn','volcanic','kababayan']#prone
    label0lst = ['sale_period','province','beautiful','ash','disaster','dangerous','bless','aurora','evacuee','plume']#sunrise

    labelscores = []
    label1score = 0;label2score = 0;label3score = 0;label4score = 0;label5score = 0;label6score = 0;label7score = 0;label8score = 0;label9score = 0;label0score = 0;
    tpclabel = []
    for x in topic:
        if(x in label1lst):
            label1score = label1score + 1
        if(x in label2lst):
            label2score = label2score + 1
        if(x in label3lst):
            label3score = label3score + 1
        if(x in label4lst):
            label4score = label4score + 1
        if(x in label5lst):
            label5score = label5score + 1
        if(x in label6lst):
            label6score = label6score + 1
        if(x in label7lst):
            label7score = label7score + 1
        if(x in label8lst):
            label8score = label8score + 1
        if(x in label9lst):
            label9score = label9score + 1
        if(x in label0lst):
            label0score = label0score + 1
    highest = max(label1score,label2score,label3score,label4score,label5score,label6score,label7score,label8score,label9score,label0score)
    #print(highest,'\n')
    #print(label1score,label2score,label3score,label4score,label5score)
    if(highest == 0):
        labelscores.append('No Label')
        labelscores.append('0')
        tpclabel.append('No Label')
        if(status==1):
            return(tpclabel)
        else:
            return(labelscores)
    if(highest == label1score):
        labelscores.append('evacuate')
        labelscores.append(label1score)
        tpclabel.append('evacuate')
    if(highest == label2score):
        labelscores.append('pray')
        labelscores.append(label2score)
        tpclabel.append('pray')
    if(highest == label3score):
        labelscores.append('augment')
        labelscores.append(label3score)
        tpclabel.append('augment')
    if(highest == label4score):
        labelscores.append('experience')
        labelscores.append(label4score)
        tpclabel.append('experience')
    if(highest == label5score):
        labelscores.append('outreach')
        labelscores.append(label5score)
        tpclabel.append('outreach')
    if(highest == label6score):
        labelscores.append('lavalflow')
        labelscores.append(label6score)
        tpclabel.append('lavaflow')
    if(highest == label7score):
        labelscores.append('suspension')
        labelscores.append(label7score)
        tpclabel.append('suspension')
    if(highest == label8score):
        labelscores.append('dangerous')
        labelscores.append(label8score)
        tpclabel.append('dangerous')
    if(highest == label9score):
        labelscores.append('prone')
        labelscores.append(label9score)
        tpclabel.append('prone')
    if(highest == label0score):
        labelscores.append('sunrise')
        labelscores.append(label0score)
        tpclabel.append('sunrise')
    #print(tpclabel)

    if(status==1):
        return(tpclabel)
    else:
        return(labelscores)

def getlbllda(topic,status):
    label1lst = ['conduct','food','chapter','aid','remain','expect','effect','plan','force','service']#support
    label2lst = ['relief','evacuation','displace','provide','show','water','disaster','ulat','abo','morning','ash','time','volcanic','spew','sign','summit','slope','warn','hour','continuosly']#lavaflow
    label3lst = ['activity','today','detail','contact','tendency','volunteer','federation','danger','enter','column']#volunteers
    label4lst = ['resident','include','province','school','distribute','tourist','increase','mask','north','majestic']#mask
    label5lst = ['people','family','evacuate','donation','affect','home','permanent','student','thousand','benificiary']#beneficiaries
    label6lst = ['alert_level','good','local','authority','raise','beautiful','work','fascinating','menacing','collectively']#linkages
    label7lst = ['volcano','philippine','stay','city','support','week','live','active','alert','mount']#alert
    label8lst = ['mayon','eruption','continue','kababayan','sunday','visit','recent','naitala','nature','posible','possible']#record
    label9lst = ['lava','safe','flow','flee','photo','danger_zone','area','reach','smoke','video']#evacuate

    
    label1score = 0;label2score = 0;label3score = 0;label4score = 0;label5score = 0;label6score = 0;label7score = 0;label8score = 0;label9score = 0;
    tpclabel = []
    labelscores = []
    #print(topic,'\n\n')
    for x in topic:
        if(x in label1lst):
            label1score = label1score + 1
        if(x in label2lst):
            label2score = label2score + 1
        if(x in label3lst):
            label3score = label3score + 1
        if(x in label4lst):
            label4score = label4score + 1
        if(x in label5lst):
            label5score = label5score + 1
        if(x in label6lst):
            label6score = label6score + 1
        if(x in label7lst):
            label7score = label7score + 1
        if(x in label8lst):
            label8score = label8score + 1
        if(x in label9lst):
            label9score = label9score + 1
    highest = max(label1score,label2score,label3score,label4score,label5score,label6score,label7score,label8score,label9score)
    #print(highest,'\n')
    #print(label1score,label2score,label3score,label4score,label5score)
    if(highest == 0):
        labelscores.append('No Label')
        labelscores.append('0')
        tpclabel.append('No Label')
        if(status==1):
            return(tpclabel)
        else:
            return(labelscores)
    if(highest == label1score):
        labelscores.append('support')
        labelscores.append(str(label1score))
        tpclabel.append('support')
    if(highest == label2score):
        labelscores.append('lavaflow')
        labelscores.append(str(label2score))
        tpclabel.append('lavaflow')
    if(highest == label3score):
        labelscores.append('volunteer')
        labelscores.append(str(label3score))
        tpclabel.append('volunteer')
    if(highest == label4score):
        labelscores.append('mask')
        labelscores.append(str(label4score))
        tpclabel.append('mask')
    if(highest == label5score):
        labelscores.append('beneficiaries')
        labelscores.append(str(label5score))
        tpclabel.append('beneficiaries')
    if(highest == label6score):
        labelscores.append('linkages')
        labelscores.append(str(label6score))
        tpclabel.append('linkages')
    if(highest == label7score):
        labelscores.append('alert')
        labelscores.append(str(label7score))
        tpclabel.append('alert')
    if(highest == label8score):
        labelscores.append('record')
        labelscores.append(str(label8score))
        tpclabel.append('record')
    if(highest == label9score):
        labelscores.append('evacuate')
        labelscores.append(str(label9score))
        tpclabel.append('evacuate')
    
    if(status==1):
        m=0
        for q in tpclabel:
            m = m  + 1
        if(m>=2):
            tpclabel = 'No Label'
        return(tpclabel)
    elif(status==2):
        return(labelscores)

def getlblldamal(topic,status):
    print('mal')
    label1lst = ['resident','area','today','live','day','video','experience','affected','view','show']#real
    label2lst = ['mayon','alert_level','evacuee','raise','remain','leave','team','learn','aalboroto','plume']#evacuate
    label3lst = ['safe','stay','beautiful','time','danger_zone','disaster','evacuation','philippine','umaga','advise','activity','family','pray','flee','affect','bulkan','province','warn','active','move']#warning
    label4lst = ['mayon','city','mocha','shelter','explosion','nature','family','beauty','pacific','video']#scenery
    label5lst = ['abo','philippine','ashfall','displace','level','safety','usok','provide','local','makapal']#support
    label6lst = ['mayon','ulat','school','alert','bless','dangerous','residente','cover','class','conduct']#advisory
    label7lst = ['lava','ash','flow','spew','town','crater','week','use','kababayan','araw']#ashfall
    label8lst = ['eruption','photo','lahar','volcanic','continue','hazardous','relief','authority','smoke','credit']#hazard
    label9lst = ['volcano','philippine','people','evacuate','home','mount','support','threat','relief_effort','local_partner']#relief
    labelscores = []
    label1score = 0;label2score = 0;label3score = 0;label4score = 0;label5score = 0;label6score = 0;label7score = 0;label8score = 0;label9score = 0;
    tpclabel = []
    #print(topic,'\n\n')
    for x in topic:
        if(x in label1lst):
            label1score = label1score + 1
        if(x in label2lst):
            label2score = label2score + 1
        if(x in label3lst):
            label3score = label3score + 1
        if(x in label4lst):
            label4score = label4score + 1
        if(x in label5lst):
            label5score = label5score + 1
        if(x in label6lst):
            label6score = label6score + 1
        if(x in label7lst):
            label7score = label7score + 1
        if(x in label8lst):
            label8score = label8score + 1
        if(x in label9lst):
            label9score = label9score + 1
    highest = max(label1score,label2score,label3score,label4score,label5score,label6score,label7score,label8score,label9score)
    #print(highest,'\n')
    #print(label1score,label2score,label3score,label4score,label5score)
    if(highest == 0):
        labelscores.append('No Label')
        labelscores.append('0')
        tpclabel.append('No Label')
        if(status==1):
            return(tpclabel)
        else:
            return(labelscores)
    elif(highest == label1score):
        labelscores.append('real')
        labelscores.append(label1score)
        tpclabel.append('real')
    elif(highest == label2score):
        labelscores.append('evacuate')
        labelscores.append(label2score)
        tpclabel.append('evacuate')
    elif(highest == label3score):
        labelscores.append('warning')
        labelscores.append(label3score)
        tpclabel.append('warning')
    elif(highest == label4score):
        labelscores.append('scenery')
        labelscores.append(label4score)
        tpclabel.append('scenery')
    elif(highest == label5score):
        labelscores.append('support')
        labelscores.append(label5score)
        tpclabel.append('support')
    elif(highest == label6score):
        labelscores.append('advisory')
        labelscores.append(label6score)
        tpclabel.append('advisory')
    elif(highest == label7score):
        labelscores.append('ashfall')
        labelscores.append(label7score)
        tpclabel.append('ashfall')
    elif(highest == label8score):
        labelscores.append('hazard')
        labelscores.append(label8score)
        tpclabel.append('hazard')
    elif(highest == label9score):
        labelscores.append('relief')
        labelscores.append(label9score)
        tpclabel.append('relief')

    if(status==1):
        return(tpclabel)
    elif(status==2):
        return(labelscores)

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
    print(lda_model.strip('+'))
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
    print(lda_model)
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
        print(x)
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
