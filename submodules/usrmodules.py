import subprocess
import os

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
