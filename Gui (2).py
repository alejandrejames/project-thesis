from submodules import topicmodel as t2
from submodules import usrmodules as usmdls
from submodules import tooltip as ttp
import os
import subprocess
import webbrowser
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.ttk import Progressbar
import threading
import time
import queue as Queue
import pickle
import datetime
import warnings
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
warnings.filterwarnings(action="ignore",category=UserWarning,module='gensim')

main = Tk()
main.title('Topic Analysis on Mayon Volcano Tweet')
main.geometry('970x500')
main.maxsize(970,500)
main.minsize(970,500)

rows = 0
while rows<50:
    main.rowconfigure(rows, weight=1)
    main.columnconfigure(rows, weight =1)
    rows +=1

nb = ttk.Notebook(main)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

############################################################################
#Tab 1 Data Collection
############################################################################
page1 = ttk.Frame(nb)
nb.add(page1, text='Collect Data')

collect_label = Label(page1, text = "Collect Data:", fg="white",font= "Times 15 bold", bg="green",width="80")
collect_label_1 = Label(page1, pady = 10,text ="Enter keyword:",font= "Times 15 bold")
collect_label_2 = Label(page1, text = "Enter max no. of tweets:", font= "Times 15 bold")
collect_label_21 = Label(page1, text = "yyyy-mm-dd",font= "Times 12 bold")
collect_label_32 = Label(page1, pady =10 ,text = "Date",font= "Times 15 bold")
collect_label_3 = Label(page1, text = "From:", font= "Times 15 bold")
collect_label_4 = Label(page1, text = "To:", pady=10, font= "Times 15 bold")
collect_label_5 = Label(page1, text = "Filename:",pady=20, font="Times 15 bold")
collect_label_6 = Label(page1, text = ".csv",pady=20, font="Times 11 bold")
collect_button = Button(page1, text ="Collect Data",fg="white", font ="Times 15 bold", bg ="green",borderwidth=3, relief ="raised", command=lambda: dataclct2(collect_entry_1.get(), collect_entry_2.get(), collect_entry_3.get(), collect_entry_4.get(),))


collect_entry_1 = Entry(page1,width="25",bg = "green",fg="white",font ="Times 15 bold")
collect_entry_2 = Entry(page1,width="25",bg = "green",fg="white",font ="Times 15 bold")
collect_entry_2.insert(END, '100')
collect_entry_3 = Entry(page1,width="25",bg = "green",fg="white",font ="Times 15 bold")
collect_entry_3.insert(END, '2018-01-01')
collect_entry_4 = Entry(page1,width="25",bg = "green",fg="white",font ="Times 15 bold")
collect_entry_4.insert(END, '2019-01-01')
collect_entry_5 = Entry(page1, width="25",bg = "green",fg="white",font ="Times 15 bold")
collect_entry_6 = Text(page1, width=120, height=6,wrap='word')
collect_entry_6.insert(END, 'Ready')
collect_entry_6.insert(END, '....\n')
collect_entry_6.insert(END, '========================================================================================================================')
collect_entry_6.config(state=DISABLED)
collect_progressbar = Progressbar(page1, orient=HORIZONTAL,length=970,  mode='indeterminate')

collect_label.grid(row= 0, columnspan=1)
collect_label_1.grid(row=1, sticky=W)
collect_label_2.grid(row=2, sticky=W)
collect_label_21.grid(row=4, sticky=W, padx=352)
collect_label_32.grid(row=4, sticky=W)
collect_label_3.grid(row=5, sticky=W)
collect_label_4.grid(row=6, sticky=W)
collect_label_5.grid(row=7, sticky=W)
collect_label_6.grid(row=7)
collect_button.grid(row=8, column=0)

collect_entry_1.grid(row=1)
collect_entry_2.grid(row=2)
collect_entry_3.grid(row=5)
collect_entry_4.grid(row=6)
collect_entry_5.grid(row=7)
now = datetime.datetime.now()
collect_entry_5.insert(END,'collecteddata'+str(now.strftime("%Y%m%d")))
collect_entry_6.grid(row=9, pady=15)
#collect_progressbar.grid(row=10, sticky=W)

#collect_entry_1_ttp = ttp.CreateToolTip(collect_entry_1, "Query keyword found in tweets")
#collect_entry_2_ttp = ttp.CreateToolTip(collect_entry_2, "Max number of tweets to be gathered")
#collect_entry_3_ttp = ttp.CreateToolTip(collect_entry_3, "Start date of collecting")
#collect_entry_4_ttp = ttp.CreateToolTip(collect_entry_4, "End date of collecting")
#collect_entry_5_ttp = ttp.CreateToolTip(collect_entry_5, "filename of the csv file")

############################################################################
#Tab 2 Data Pre - Processing
############################################################################
page3 =  ttk.Frame(nb)
nb.add(page3, text ='Data Pre-proccessing')
dpp_frame_1 = Frame(page3)
dpp_frame_2 = Frame(page3,width=1,height=1)

dpp_label_1 = Label(page3, text="Data Pre-processing:",fg="white", font = "Times 15 bold",bg="blue",width="80")
dpp_label_2 = Label(dpp_frame_1, text="CSV Filename:", font = "Times 15 bold", pady=20)
dpp_label_3 = Label(dpp_frame_1, text="Remove:", font = "Times 15 bold")
dpp_label_4 = Label(dpp_frame_1, text="Filename for Cleaned Data", font = "Times 14 bold")
dpp_label_5 = Label(dpp_frame_1, text=".cds", font = "Times 14")
dpp_label_6 = Label(page3, text="Stopwords", font = "Times 14 bold")
dpp_label_7 = Label(page3, text="Trigram Threshold:", font = "Times 14 bold")

emailvar = IntVar()
dpp_checkbox_1 = Checkbutton(dpp_frame_1, text = "Username", font = "Times 15", variable=emailvar)
dpp_checkbox_1.select()
speccharvar = IntVar()
dpp_checkbox_2 = Checkbutton(dpp_frame_1, text = "Special characters(ex:@#!$%^)", font = "Times 15", variable=speccharvar)
dpp_checkbox_2.select()
linkvar = IntVar()
dpp_checkbox_3 = Checkbutton(dpp_frame_1, text = "Links", font = "Times 15", variable=linkvar)
dpp_checkbox_3.select()
stpwrdvar = IntVar()
dpp_checkbox_4 = Checkbutton(dpp_frame_1, text = "Remove Stopwords", font = "Times 15", variable=stpwrdvar)
dpp_checkbox_4.select()

dpp_entry_1 = Entry(dpp_frame_1,width="25",bg="blue",fg="white",font = "Times 15 bold")
dpp_entry_1.insert(END, 'orginaldata.csv')
dpp_entry_2 = Entry(dpp_frame_1,width="25",bg="blue",fg="white",font = "Times 15 bold")
dpp_entry_2.insert(END, 'cleaneddata')
dpp_scrollbar = Scrollbar(page3)
dpp_entry_3 = usmdls.CustomText(page3,width=75,height=15,font = "Times 10",yscrollcommand = dpp_scrollbar.set)
dpp_entry_3.tag_configure("yellow", background="#FFFF00",foreground="#000000")
dpp_entry_4 = Text(page3,width=159,height=5,font = "Times 10")
dpp_entry_4.insert(END, 'Ready')
dpp_entry_4.insert(END, '....\n')
dpp_entry_4.insert(END, '========================================================================================================================================')
dpp_entry_4.config(state=DISABLED)
cleaning_progressbar = Progressbar(page3, orient=HORIZONTAL,length=970,  mode='indeterminate')
dpp_scrollbar.config(command = dpp_entry_3.yview)

dpp_button_1 = Button(page3, text ="Default Stopwords",fg="white", font ="Times 12 bold", borderwidth=2, relief ="raised",bg ="blue", command=lambda: viewstopwrds(main,1))
dpp_button_2 = Button(page3, text ="User Defined Stopwords",fg="white", font ="Times 12 bold", borderwidth=2, relief ="raised",bg ="blue", command=lambda: viewstopwrds(main,2))
dpp_button_3 = Button(dpp_frame_1, text ="Clean Data  File",fg="white", font ="Times 15 bold", borderwidth=3, relief ="raised",bg ="blue", padx=30, command=lambda: datacleaning2(main,dpp_entry_1.get()))
dpp_button_4 = Button(page3, text ="Tagalog Stopwords",fg="white", font ="Times 12 bold", borderwidth=2, relief ="raised",bg ="blue", command=lambda: viewstopwrds(main,3))

dpp_button_import = Button(page3,text="Import a Dataset",command= lambda:importdataset())

dpp_label_1.grid(row=0, sticky=W)

dpp_frame_1.grid(row=3, sticky=W)
dpp_label_2.grid(row=0,sticky=W)
dpp_entry_1.grid(row=0,sticky=W,padx=130)
dpp_label_3.grid(row=1,sticky=W)
dpp_button_import.grid(row=2,sticky=W,padx=20)
dpp_checkbox_1.grid(row=2,sticky=W)
dpp_checkbox_2.grid(row=2,sticky=W,padx=110)
dpp_checkbox_3.grid(row=3,sticky=W)
dpp_checkbox_4.grid(row=3,sticky=W,padx=110)
dpp_label_4.grid(row=4,sticky=W)
dpp_entry_2.grid(row=5,sticky=W,padx=20)
dpp_label_5.grid(row=5,sticky=W,padx=270)
dpp_button_3.grid(row=6,sticky=W,padx=40,pady=15)

dpp_label_6.grid(row=1,sticky=W,padx=500)
dpp_button_1.grid(row=2,sticky=W,padx=500)
dpp_button_2.grid(row=2,sticky=W,padx=640)
dpp_button_4.grid(row=2,sticky=W,padx=820)
dpp_entry_3.grid(row=3,sticky=W,padx=490)
dpp_scrollbar.grid(row=3,sticky=W,padx=950,ipady=100)

dpp_entry_4.grid(row=5, sticky=W)
#cleaning_progressbar.grid(row=6,sticky=W)



#dpp_entry_1_ttp = ttp.CreateToolTip(dpp_entry_1, "Filename of the csv file to be  cleaned")
#dpp_entry_2_ttp = ttp.CreateToolTip(dpp_entry_2, "Ignore all words and bigrams with total collected count lower than this value.")
#dpp_entry_3_ttp = ttp.CreateToolTip(dpp_entry_3, "Bigram score threshold for forming the phrases (higher means fewer phrases). A phrase of words a followed by b is accepted if the score of the phrase is greater than threshold. Heavily depends on concrete scoring-function, see the scoring parameter.")
#dpp_entry_4_ttp = ttp.CreateToolTip(dpp_entry_4, "Trigram score threshold for forming the phrases (higher means fewer phrases). A phrase of words a followed by b is accepted if the score of the phrase is greater than threshold. Heavily depends on concrete scoring-function, see the scoring parameter.")


#######################################################################
page2 =  ttk.Frame(nb)
nb.add(page2, text ='Generate Topic Models')
tpcmdl_label_1 = Label(page2, text ="Generate topics using LDA and NMF", font= "Times 15 bold" ,bg="grey",width=90, fg="white")
tpcmdl_label_2 = Label(page2, text = "Enter no. of topics:",pady=30, font= "Times 15 bold")
tpcmdl_button = Button(page2, text ="Browse", font ="Times 15 bold", borderwidth=3, relief="solid")
tpcmdl_button1 = Button(page2, text ="Generate Topic Keywords", font ="Times 15 bold",bg="grey",fg="white", borderwidth=3, relief="raised", command=lambda: genertp2(tpcmdl_entry_1.get()))
tpcmdl_label_3 = Label(page2, text = "Filename:",pady=10, font= "Times 15 bold")
tpcmdl_entry_1 = Entry(page2, width ="25",bg="grey",fg="white",font = "Times 15 bold")
tpcmdl_entry_1.insert(END,'cleaneddata.cds')
tpcmdl_entry_2 = Entry(page2, width ="20",font= "Times 15 bold")
tpcmdl_entry_4 = Text(page2,width=160,height=10,font = "Times 10")
tpcmdl_entry_4.insert(END, 'Ready')
tpcmdl_entry_4.insert(END, '....\n')
tpcmdl_entry_4.insert(END, '=========================================================================================================================================')
tpcmdl_entry_4.config(state=DISABLED)
tpcmdl_progressbar = Progressbar(page2, orient=HORIZONTAL,length=970,  mode='indeterminate')

tpcmdl_label_4 = Label(page2, text = "Parameters",pady=10, font= "Times 15 bold")
ldaparam_label_1 = Label(page2, text = "Num. Topics:",pady=3, font= "Times 14 bold")
ldaparam_entry_1 = Entry(page2,bg="grey",fg="white", width ="6",font= "Times 15 bold")
ldaparam_entry_1.insert(END,int(10))
ldaparam_label_2 = Label(page2, text = "Random State:",pady=3, font= "Times 14 bold")
ldaparam_entry_2 = Entry(page2,bg="grey",fg="white", width ="15",font= "Times 15 bold")
ldaparam_entry_2.insert(END,int(1000))
ldaparam_label_3 = Label(page2, text = "Iterations:",pady=3, font= "Times 14 bold")
ldaparam_entry_3 = Entry(page2,bg="grey",fg="white", width ="15",font= "Times 15 bold")
ldaparam_entry_3.insert(END,int(500))
ldaparam_label_4 = Label(page2, text = "Chunk Size",pady=3, font= "Times 14 bold")
ldaparam_entry_4 = Entry(page2,bg="grey",fg="white", width ="15",font= "Times 15 bold")
ldaparam_entry_4.insert(END,int(100))
ldaparam_label_5 = Label(page2, text = "Training Passes:",pady=3, font= "Times 14 bold")
ldaparam_entry_5 = Entry(page2, bg="grey",fg="white",width ="15",font= "Times 15 bold")
ldaparam_entry_5.insert(END,int(10))
ldaparam_label_6 = Label(page2, text = "Word Per Topic:",pady=3, font= "Times 14 bold")
ldaparam_entry_6 = Entry(page2,bg="grey",fg="white", width ="6",font= "Times 15 bold")
ldaparam_entry_6.insert(END,int(10))
ldaparam_label_7 = Label(page2, text = "LDA Model:",pady=3, font= "Times 14 bold")
ldaparam_opmenu_variable = StringVar(page2)
ldaparam_opmenu_variable.set("Gensim") # default value
ldaparam_opmenu = OptionMenu(page2, ldaparam_opmenu_variable, "Gensim", "Mallet")

tpcmdl_label_5 = Label(page2, text = "Algorithm",pady=10, font= "Times 15 bold")
nmfparam_label_1 = Label(page2, text = "Num. Topics:",pady=3, font= "Times 14 bold")
nmfparam_entry_1 = Entry(page2,bg="grey",fg="white", width ="5",font= "Times 15 bold")
nmfparam_entry_1.insert(END,int(10))
nmfparam_label_2 = Label(page2, text = "Vectorizer Max Features:",pady=3, font= "Times 14 bold")
nmfparam_entry_2 = Entry(page2,font= "Times 15 bold",bg="grey",fg="white")
nmfparam_entry_2.insert(END,int(5000))
nmfparam_label_3 = Label(page2, text = "Word per topic:",pady=3, font= "Times 14 bold")
nmfparam_entry_3 = Entry(page2,bg="grey",fg="white", font= "Times 15 bold",width='5')
nmfparam_entry_3.insert(END,int(10))
nmfparam_label_4 = Label(page2, text = "Iterations:",pady=3, font= "Times 14 bold")
nmfparam_entry_4 = Entry(page2,bg="grey",fg="white", font= "Times 15 bold")
nmfparam_entry_4.insert(END,int(500))
nmfparam_label_5 = Label(page2, text = "Random State:",pady=3, font= "Times 14 bold")
nmfparam_entry_5 = Entry(page2,bg="grey",fg="white", font= "Times 15 bold")
nmfparam_entry_5.insert(END,int(random.randint(1,101)))

v = IntVar()
tpcmdl_radio1 = tk.Radiobutton(page2, text="Latent Dirichlet Allocation(LDA)",font= "Times 14 bold", variable=v, value=1,command=lambda:switchmenu("LDA"));
tpcmdl_radio2 = tk.Radiobutton(page2, text="Non-negative Matrix Factorization(NMF)",font= "Times 14 bold", variable=v, value=2,command=lambda:switchmenu("NMF"))
tpcmdl_radio1.select()
tpcmdl_label_6 = Label(page2,text="Labelling Settings",font= "Times 14 bold")
ckboxvar = IntVar()
tpcmdl_ckbox =Checkbutton(page2, text = "Show available labels instead of 'No Labels' for topics that has 2 labels", variable=ckboxvar)
tpcmdl_lblbutton = Button(page2, text ="Label List",command = lambda: viewalllabels())
tpcmdl_lblbutton2 = Button(page2, text ="Add New Label",command=lambda: addnewlabel())
tpcmdl_lblbutton3 = Button(page2, text ="Remove a Label",command=lambda: remlabel())

tpcmdl_label_1.grid(row=0, sticky=W)
tpcmdl_label_3.grid(row=1,sticky=W)
tpcmdl_entry_1.grid(row=1,sticky=W,padx=90)

tpcmdl_label_4.grid(row=2,sticky=W)
ldaparam_label_1.grid(row=3,sticky=W)
ldaparam_entry_1.grid(row=3,sticky=W,padx=115)
ldaparam_label_6.grid(row=3,sticky=W,padx=185)
ldaparam_entry_6.grid(row=3,sticky=W,padx=330)
ldaparam_label_3.grid(row=4,sticky=W)
ldaparam_entry_3.grid(row=4,sticky=W,padx=90)
ldaparam_label_5.grid(row=5,sticky=W)
ldaparam_entry_5.grid(row=5,sticky=W,padx=140)
ldaparam_label_7.grid(row=7,sticky=W)
ldaparam_opmenu.grid(row=7,sticky=W,padx=120)

tpcmdl_label_5.grid(row=1,sticky=W,padx=525)
tpcmdl_radio1.grid(row=2,sticky=W,padx=525)
tpcmdl_radio2.grid(row=3,sticky=W,padx=525)
tpcmdl_label_6.grid(row=4,sticky=W,padx=525)
tpcmdl_ckbox.grid(row=5,sticky=W,padx=525)
tpcmdl_lblbutton2.grid(row=6,sticky=W,padx=525)
tpcmdl_lblbutton.grid(row=6,sticky=W,padx=640)
tpcmdl_lblbutton3.grid(row=6,sticky=W,padx=740)

#nmfparam_label_1.grid(row=3,sticky=W,padx=525)
#nmfparam_entry_1.grid(row=3,sticky=W,padx=640)
#nmfparam_label_3.grid(row=3,sticky=W,padx=700)
#nmfparam_entry_3.grid(row=3,sticky=W,padx=835)
#nmfparam_label_2.grid(row=4,sticky=W,padx=525)
#nmfparam_entry_2.grid(row=4,sticky=W,padx=745)
#nmfparam_label_4.grid(row=5,sticky=W,padx=525)
#nmfparam_entry_4.grid(row=5,sticky=W,padx=615)


tpcmdl_button1.grid(row=8,sticky=W,padx=340)
tpcmdl_entry_4.grid(row=9, sticky=W,pady=8)
#tpcmdl_progressbar.grid(row=10,sticky=W)


#tpcmdl_entry_1_ttp = ttp.CreateToolTip(tpcmdl_entry_1, "File name of the cleaned data set")
#ldaparam_entry_1_ttp = ttp.CreateToolTip(ldaparam_entry_1, "The number of requested latent topics to be extracted from the training corpus.")
#ldaparam_entry_2_ttp = ttp.CreateToolTip(ldaparam_entry_2, "Random state is the seed used by the random number generator")
#ldaparam_entry_3_ttp = ttp.CreateToolTip(ldaparam_entry_3, "Number of documents to be iterated through for each update. Set to 0 for batch learning, > 1 for online iterative learning")
#ldaparam_entry_4_ttp = ttp.CreateToolTip(ldaparam_entry_4, "Number of documents to be used in each training chunk.")
#ldaparam_entry_5_ttp = ttp.CreateToolTip(ldaparam_entry_5, "Number of passes through the corpus during training")
#ldaparam_entry_6_ttp = ttp.CreateToolTip(ldaparam_entry_6, "Number of words to be generated per topic")
#nmfparam_entry_1_ttp = ttp.CreateToolTip(nmfparam_entry_1, "Number of topics to be generated by the model")
#nmfparam_entry_2_ttp = ttp.CreateToolTip(nmfparam_entry_2, "Builds a vocabulary that only consider the top max_features ordered by term frequency across the corpus")
#nmfparam_entry_3_ttp = ttp.CreateToolTip(nmfparam_entry_3, "When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words). Minimum value")
#nmfparam_entry_4_ttp = ttp.CreateToolTip(nmfparam_entry_4, "When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words). Maximum value must be in float and higher than min value")

#############################################################################
##Script Functions
#############################################################################
#
#Generate Topic Models Ver.2
def genertp2(name):
    def viewpyldavis():
        new=2
        webbrowser.open('LDA_Visualization.html',new=new)
    def freqbar(model):
        if(model=='lda'):
            usmdls.ldafreqbar()
        else:
            usmdls.nmffreqbar()
    def viewwrcld(model):
        if(model=='lda'):
            with open('ldamdl.lda', 'rb') as filehandle:
                lda_model = pickle.load(filehandle)
            title = 'Latent Dirichlet Allocation(LDA) WordCloud'
            wordcloud = WordCloud(background_color='white',max_font_size=40, scale=3,random_state=1,width=800,height=400).generate(str(lda_model))
            fig = plt.figure(1, figsize=(20, 10))
            plt.axis('off')
            plt.imshow(wordcloud)
            plt.savefig('ldawc')
            plt.show()
        else:
            with open('nmfmdl.nmf', 'rb') as filehandle:
                lda_model = pickle.load(filehandle)
            title = 'Non-negative Matrix Factorization(NMF) WordCloud'
            wordcloud = WordCloud(background_color='white',max_font_size=40, scale=3,random_state=1,width=800,height=400).generate(str(lda_model))
            fig = plt.figure(1, figsize=(20, 10))
            plt.axis('off')
            plt.imshow(wordcloud)
            plt.savefig('nmfwc')
            plt.show()
    def openresultwindow():
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"),width=580,height=590)
        algotbused = v.get()
        window1 = tk.Toplevel(main)
        window1.title('Topic Analysis on Mayon Volcano Tweet')
        window1.geometry('1300x600')
        window1.maxsize(620,600)
        window1.minsize(620,600)

        myframe=Frame(window1,relief=GROOVE,width=50,height=100,bd=1)
        myframe.place(x=0,y=0)

        canvas=Canvas(myframe)
        window=Frame(canvas)
        myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="left")
        canvas.create_window((0,0),window=window,anchor='nw')
        window.bind("<Configure>",myfunction)
        
        result_label_1 = Label(window,text = 'Generated Results')
        result_label_1.grid(row=0,sticky=W,padx=240)

        if(algotbused==1):
            result_button_1 = Button(window,text='Visualize LDA in WordCloud' ,command= lambda:viewwrcld('lda'))
            result_button_1.grid(row=1,sticky=W,padx=10)
            result_button_2 = Button(window,text='View LDA Word Frequency in Matplotlib',command= lambda:freqbar('lda'))
            result_button_2.grid(row=1,sticky=W,padx=360)
            result_button_3 = Button(window,text='View in pyLDAvis Chart',command= lambda:viewpyldavis())
            result_button_3.grid(row=2,sticky=W,padx=10,pady=5)

            result_label_2 = Label(window,text = 'LDA Result')
            result_label_2.grid(row=3,sticky=W,pady=20,padx=250)

            result_label_4 = Label(window,text = 'Topic Number')
            result_label_4.grid(row=4,sticky=W)
            result_label_5 = Label(window,text = 'Topic Words')
            result_label_5.grid(row=4,sticky=W,padx=100)
            result_label_6 = Label(window,text = 'Labels')
            result_label_6.grid(row=4,sticky=W,padx=450)

            numrows = 5
            labelsLDA = []
            textasLDA = []
            entriesLDA = []
            fl3 = open('ldaresult.res','r')
            hitwrd = open('hitwordsLDA.txt','a')
            conts = fl3.readline()
            flag=0
            num = 0
            topicsg = []
            topicswrd = []
            for x in conts:
                if(x=='('):
                    label = Label(window,text='Topic'+str(num))
                    texta = Text(window,height=3,width=40)
                    entry = Entry(window)
                elif(x==')'):
                    labelsLDA.append(label)
                    textasLDA.append(texta)
                    entriesLDA.append(entry)
                    num = int(num) + 1
                    hitwrd.write('[]')
                    if(ldaparam_opmenu_variable.get() == 'Gensim'):
                        entry.insert(END,usmdls.getlbllda(topicsg,1,ckboxvar.get()))
                    else:
                        entry.insert(END,usmdls.getlblldamal(topicsg,1,ckboxvar.get()))
                    topicsg = []
                elif(x=='*'):
                    continue
                    #texta.insert(END,'-')
                elif(x=='+'):
                    texta.insert(END,',')
                    hitwrd.write(',')
                    charstr = ''.join(topicswrd)
                    topicsg.append(charstr)
                    topicswrd = []
                elif(x==','):
                    q = 0
                elif(x==' '):
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
                    if(x=='0' or x=='1' or x=='2' or x=='3' or x=='4' or x=='5' or x=='6' or x=='7' or x=='8' or x=='9' or x=='.'):
                        continue
                    else:
                        texta.insert(END,x)
                        topicswrd.append(x)
                        hitwrd.write(x)
            hitwrd.write('-')
            hitwrd.close()
            fl3.close()
            count = 0
            for m in labelsLDA:
                m.grid(row=numrows+count,sticky=W)
                count =count + 1
            
            count = 0
            for m in textasLDA:
                m.grid(row=numrows+count,sticky=W,padx=100)
                count =count + 1
            
            count = 0
            for m in entriesLDA:
                m.grid(row=numrows+count,sticky=W,padx=450)
                count =count + 1
        else:
            result_button_4 = Button(window,text='Visualize NMF in WordCloud',command= lambda:viewwrcld('nmf'))
            result_button_4.grid(row=1,sticky=W,padx=10)
            result_button_5 = Button(window,text='View NMF Word Frequency in Matplotlib',command= lambda:freqbar('nmf'))
            result_button_5.grid(row=1,sticky=W,padx=360)

            result_label_3 = Label(window,text = 'NMF Result')
            result_label_3.grid(row=2,sticky=W,pady=20,padx=250)
            
            result_label_4 = Label(window,text = 'Topic Number')
            result_label_4.grid(row=3,sticky=W)
            result_label_5 = Label(window,text = 'Topic Words')
            result_label_5.grid(row=3,sticky=W,padx=100)
            result_label_6 = Label(window,text = 'Labels')
            result_label_6.grid(row=3,sticky=W,padx=450)

            #NMF
            numrows = 4
            labelsNMF = []
            textasNMF = []
            entriesNMF = []
            fl = open('nmfresult.res','r')
            hitwrd = open('hitwordsNMF.txt','a')
            conts = fl.readline()
            flag=0
            num = 0
            topicsg = []
            topicwrd = []
            for x in conts:
                if(x=='['):
                    label = Label(window,text='Topic'+str(num))
                    texta = Text(window,height=3,width=40)
                    entry = Entry(window)
                elif(x==']'):
                    labelsNMF.append(label)
                    textasNMF.append(texta)
                    entriesNMF.append(entry)
                    num = int(num) + 1
                    hitwrd.write('[]')
                    #print(topicsg,'\n\n')
                    entry.insert(END,usmdls.getlblnmf(topicsg,1,ckboxvar.get()))
                    topicsg = []
                elif(x==","):
                    q = 0
                    charstr = ''.join(topicwrd)
                    #print(charstr)
                    topicsg.append(charstr)
                    topicwrd = []
                    texta.insert(END,',')
                elif(x=='\''):
                    continue
                elif(x==' '):
                    continue
                else:
                    texta.insert(END,x)
                    topicwrd.append(x)
                    hitwrd.write(x)
            hitwrd.write('-')
            hitwrd.close()
            fl.close()
                
            count = 0
            for m in labelsNMF:
                m.grid(row=numrows+count,sticky=W)
                count =count + 1
            
            count = 0
            for m in textasNMF:
                m.grid(row=numrows+count,sticky=W,padx=100)
                count =count + 1
            
            count = 0
            for m in entriesNMF:
                m.grid(row=numrows+count,sticky=W,padx=450)
                count =count + 1
    def topicmdling(name):
        tpcmdl_entry_4.insert(END,'Reading file contents...')
        with open(name, 'rb') as filehandle:
            cleaned = pickle.load(filehandle)
        tpcmdl_entry_4.insert(END,'Success\n')
        tpcmdl_entry_4.see(tk.END)
        corpus = t2.mkcorpus(cleaned)
        algotbused = v.get()
        print(algotbused)
        if(algotbused==1):
            if(ldaparam_opmenu_variable.get()=='Gensim'):
                tpcmdl_entry_4.insert(END,'LDA Training...')
                tpcmdl_entry_4.see(END)
                outres1 = t2.ldamdl(corpus,cleaned,int(ldaparam_entry_1.get()) ,int(ldaparam_entry_2.get()) ,int(ldaparam_entry_3.get()) ,int(ldaparam_entry_5.get()) ,int(ldaparam_entry_6.get()))
            else:
                tpcmdl_entry_4.insert(END,'LDA Training...')
                tpcmdl_entry_4.see(tk.END)
                outres1 = t2.mallda(corpus,cleaned,int(ldaparam_entry_1.get()),int(ldaparam_entry_6.get()),int(ldaparam_entry_3.get()))
            fl1 = open("ldaresult.res","w")
            fl1.write("".join(outres1))
            fl1.close()
            tpcmdl_entry_4.insert(END,'Success\n')
            tpcmdl_entry_4.see(tk.END)
        else:
            tpcmdl_entry_4.insert(END,'NMF Training...')
            tpcmdl_entry_4.see(tk.END)
            outres2 =t2.nmfmdl(cleaned,int(nmfparam_entry_1.get()) ,int(nmfparam_entry_2.get()),int(nmfparam_entry_3.get()) ,int(nmfparam_entry_4.get()),int(nmfparam_entry_5.get()))
            fl2 = open("nmfresult.res","w")
            fl2.writelines("".join(outres2))
            fl2.close()
            tpcmdl_entry_4.insert(END,'Success\n')
            tpcmdl_entry_4.see(tk.END)
            tpcmdl_entry_4.insert(END,'Generating Results...')
            tpcmdl_entry_4.see(tk.END)
            
        genresults()
        tpcmdl_entry_4.insert(END,'Success\n')
        tpcmdl_entry_4.see(tk.END)

    class ThreadedTask(threading.Thread):
        def __init__(self, queue):
            threading.Thread.__init__(self)
            self.queue = queue
        def run(self):
            topicmdling(name)  # Simulate long running process
            tpcmdl_entry_4.insert(END,'Completed')
            tpcmdl_entry_4.see(tk.END)
            tpcmdl_entry_4.config(state='disabled')
            tpcmdl_progressbar.stop()
            openresultwindow()
            
    tpcmdl_entry_4.config(state='normal')
    tpcmdl_entry_4.see(tk.END)
    text = "Parameters:\n"
    tpcmdl_entry_4.insert(END,text)
    text = "LDA: Number of topics="+ldaparam_entry_1.get()+", Word Per Topic="+ldaparam_entry_6.get()+", Iterations="+ldaparam_entry_3.get()+", Training Passes="+ldaparam_entry_5.get()+", Random State="+ldaparam_entry_2.get()+", LDA Model="+ldaparam_opmenu_variable.get()+"\n"
    tpcmdl_entry_4.insert(END,text)
    text = "NMF: Number of topics="+nmfparam_entry_1.get()+", Word Per Topic="+nmfparam_entry_3.get()+", Vectorizer Max Features="+nmfparam_entry_2.get()+", Iterations="+ldaparam_entry_4.get()+", Random State="+nmfparam_entry_5.get()+"\n"
    tpcmdl_entry_4.insert(END,text)
    tpcmdl_progressbar.start()
    ThreadedTask(tpcmdl_entry_4).start()
#####################################################################################
#
#Data Collection Ver.2
def dataclct2(query,num,startd,endd):
    def opendir(window):
        dir_path = os.path.dirname(os.path.realpath(__file__))# open current directory
        subprocess.check_call(['explorer', dir_path])
        window.destroy()
    def openfl():
        os.system("start EXCEL.EXE "+collect_entry_5.get()+".csv")
        #os.system("start EXCEL.EXE "+"orginaldata.csv")
    def collection(query,num,startd,endd): 
        usmdls.collectdata(query,num,startd,endd,collect_entry_5.get())
    def process_queue(self):
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            self.prog_bar.stop()
        except Queue.Empty:
            self.master.after(100, self.process_queue)

    class ThreadedTask(threading.Thread):
        def __init__(self, queue):
            threading.Thread.__init__(self)
            self.queue = queue
        def run(self):
            collect_progressbar.start()
            collection(query,num,startd,endd)  # Simulate long running process
            collect_progressbar.stop()
            text = "Completed\n"
            collect_entry_6.insert(END,text)
            collect_entry_6.config(state='disabled')
            
            window = tk.Toplevel(main)
            window.title('Completed')
            window.minsize(1200,500)
            window.maxsize(1200,500)
            windowstatus_label = Label(window, text = "Collected Tweets",pady=10, font= "Times 11")
            viewresults2_button = Button(window, text ="Open in Explorer", font ="Times 11", borderwidth=3, command=lambda: opendir(window2))
            openfile_button = Button(window, text ="Open File", font ="Times 11", borderwidth=3, command=lambda: openfl())
            windowlabel_1 = Label(window,text='Twittter Data')
            
            windowstatus_label.grid(row=0,sticky=W)
            viewresults2_button.grid(row=1,sticky=W)
            openfile_button.grid(row=2,sticky=W)
            windowlabel_1.grid(row=3,sticky=W)
            scrollbar = Scrollbar(window)
            text1 = Text(window,width=145,height=21,yscrollcommand = scrollbar.set)
            text1.grid(row=4,sticky=W,padx=10,pady=5)
            scrollbar.grid(row=4,sticky=W,ipady=150,padx=1178)
            scrollbar.config(command = text1.yview)

            csvname = collect_entry_5.get()+'.csv'
            #data = pd.read_csv('orginaldata.csv', error_bad_lines=False)
            data = pd.read_csv(csvname, error_bad_lines=False)
            # We only need the Headlines text column from the data
            data_text = data[['data','username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink']]
            data_text = data_text.astype('str');
            data = data_text.data.values.tolist()
            numb=0
            for x in data:
                if(x!='nan'):
                    textstr = 'Tweet No. '+str(numb)+' - '+data[numb]+'\n\n'
                    text1.insert(END,textstr)
                numb = numb + 1
            
            
            entrywrd = collect_entry_5.get()+".csv"
            dpp_entry_1.delete(0, tk.END)
            dpp_entry_1.insert(0, entrywrd)
            
    collect_entry_6.config(state='normal')
    text = "Parameters: Searchquery="+query+" ,Max No. of Tweets="+num+" ,From="+startd+" ,Until="+endd+"\n"
    collect_entry_6.see(tk.END)
    collect_entry_6.insert(END,text)
    collect_entry_6.see(tk.END)
    text = "Collecting....\n"
    collect_entry_6.see(tk.END)
    collect_entry_6.insert(END,text)
    collect_entry_6.see(tk.END)
    ThreadedTask(collect_entry_6).start()
#########################################################################################################
#
#Generate Results Function
def genresults():
    resultpg = open('viewresults.html','w')
    
    fpart = open('HTMLFiles/firstpart.html','r')
    fpartr = fpart.read()
    
    resultpg.write(fpartr)
    fpart.close

    usmdls.ldaout(resultpg)

    mpart = open('HTMLFiles/midpart.html','r')
    mpartr = mpart.read()

    resultpg.write(mpartr)
    mpart.close

    usmdls.nmfout(resultpg)

    lpart = open('HTMLFiles/lastpart.html','r')
    lpartr = lpart.read()
    
    resultpg.write(lpartr)
    lpart.close

    resultpg.close()
#######################################################################################
#
#Data Cleaning Ver.2
def datacleaning2(main,name):
    def openfl(window):
        os.system("start EXCEL.EXE "+"cleaneddataset-readable"+".csv")
        window.destroy()
    def cleaningdata(name):
        cleaned = t2.cleaning(name,emailvar.get(),linkvar.get(),speccharvar.get(),stpwrdvar.get(),dpp_entry_4)
        fname = dpp_entry_2.get()+".cds"
        with open(fname,"wb") as filehandle:
            pickle.dump(cleaned,filehandle,protocol=pickle.HIGHEST_PROTOCOL)
    class ThreadedTask(threading.Thread):
        def __init__(self, queue):
            threading.Thread.__init__(self)
            self.queue = queue
        def run(self):
            cleaningdata(name)# Simulate long running process
            cleaning_progressbar.stop()
            dpp_entry_4.insert(END,'Completed')
            dpp_entry_4.see(tk.END)
            dpp_entry_4.config(state='disabled')
            window = tk.Toplevel(main)
            window.title('Cleaning Results')
            window.minsize(1000,500)
            window.maxsize(1000,500)
            window_label = Label(window, text = "Cleaned Data Set",pady=10, font= "Times 11")
            window_scrollbar_1 = Scrollbar(window)
            window_entry = Text(window,width=160,height=15,font = "Times 10",yscrollcommand=window_scrollbar_1.set)
            window_scrollbar_1.config(command=window_entry.yview)
            window_label_2 = Label(window, text = "Removed Words",pady=10, font= "Times 11")
            window_scrollbar_2 = Scrollbar(window)
            window_entry_2 = Text(window,width=160,height=7,font = "Times 10",yscrollcommand=window_scrollbar_2.set)
            window_scrollbar_2.config(command=window_entry_2.yview)
            window_button = Button(window, text ="Open in notepad", font ="Times 11", borderwidth=3, command=lambda: openfl(window))
            window_button_2 = Button(window, text ="Close", font ="Times 11", borderwidth=3, command=lambda: window.destroy())
            
            window_label.grid(row=0,sticky=W)
            window_button.grid(row=0,sticky=W,padx=750)
            window_button_2.grid(row=0,sticky=W,padx=880)
            window_entry.grid(row=1,sticky=W,padx=10)
            window_scrollbar_1.grid(row=1,sticky=W,padx=975,ipady=90)
            window_label_2.grid(row=2,sticky=W)
            window_entry_2.grid(row=3,sticky=W,padx=10)
            window_scrollbar_2.grid(row=3,sticky=W,padx=975,ipady=40)
            
            
            with open("cleaneddata.cds","rb") as filehandle:
                words = pickle.load(filehandle)
            window_entry.insert(END,words)
            
            with open("additional_stop_words_mallet.asw","r") as filehandle:
                rwords = filehandle.readlines()
            window_entry_2.insert(END,rwords)
            with open("additional_stop_words_tagalog.asw","r") as filehandle:
                rwords = filehandle.readlines()
            window_entry_2.insert(END,rwords)
            with open("additional_stop_words.asw","r") as filehandle:
                rwords = filehandle.readlines()
            window_entry_2.insert(END,rwords)
            window_entry.config(state='disabled')
            window_entry_2.config(state='disabled')
            
            entrywrd = dpp_entry_2.get()+".cds"
            tpcmdl_entry_1.delete(0, tk.END)
            tpcmdl_entry_1.insert(0, entrywrd)
            
    dpp_entry_4.config(state='normal')
    cleaning_progressbar.start()
    text = "Parameters: Filename="+name+","
    if(emailvar.get() == 1):
        text = text+" Remove Usernames=Yes,"
    else:
        text = text+" Remove Usernames=No,"
    if(linkvar.get() == 1):
        text = text+" Remove Links=Yes,"
    else:
        text = text+" Remove Links=No,"
    if(speccharvar.get() == 1):
        text = text+" Remove Special Characters=Yes,"
    else:
        text = text+" Remove Special Characters=No,"
    if(stpwrdvar.get() == 1):
        text = text+" Remove Stopwords=Yes\n"
    else:
        text = text+" Remove Stopwords=No\n"
    dpp_entry_4.insert(END,text)
    dpp_entry_4.see(tk.END)
    ThreadedTask(dpp_entry_4).start()
############################################################################
#
#Stopwords Viewing
def viewstopwrds(main,stats):
    def updatestpwrds(stpwrds_extension,stats):
        if(stats==3):
            with open("additional_stop_words_tagalog.asw","w") as filehandle:
                filehandle.write(stpwrds_extension)
            dpp_entry_4.config(state='normal')
            dpp_entry_4.insert(END,'Stopwords Updated\n')
            dpp_entry_4.see(tk.END)
            dpp_entry_4.config(state='disabled')
        elif(stats==2):
            with open("additional_stop_words.asw","w") as filehandle:
                filehandle.write(stpwrds_extension)
            dpp_entry_4.config(state='normal')
            dpp_entry_4.insert(END,'Stopwords Updated\n')
            dpp_entry_4.see(tk.END)
            dpp_entry_4.config(state='disabled')
        else:
            with open("additional_stop_words_mallet.asw","w") as filehandle:
                filehandle.write(stpwrds_extension)
            dpp_entry_4.config(state='normal')
            dpp_entry_4.insert(END,'Stopwords Updated\n')
            dpp_entry_4.see(tk.END)
            dpp_entry_4.config(state='disabled')

        dpp_button_5.grid_remove()
        dpp_entrysearch.grid_remove()
        dpp_button_6.grid_remove()
        dpp_button_1.grid(row=2,sticky=W,padx=500)
        dpp_button_2.grid(row=2,sticky=W,padx=640)
        dpp_button_4.grid(row=2,sticky=W,padx=820)
        dpp_entry_3.delete("1.0", tk.END)
    def findtext(txtsrch):
        def dothisfrst():
            dpp_entry_3.tag_add("here", "1.0", END)
            dpp_entry_3.tag_config("here",foreground="black",background="white")
            dpp_entry_3.tag_remove("here", "1.0", END)
        dothisfrst()
        dpp_entry_3.tag_configure("yellow", background="#FFFF00",foreground="#000000")
        dpp_entry_3.highlight_pattern(txtsrch,"yellow")
    dpp_button_5 = Button(page3, text ="Update Stopwords",fg="white", font ="Times 12 bold", borderwidth=2, relief ="raised",bg ="blue", command=lambda: updatestpwrds(dpp_entry_3.get("1.0",END),stats))
    dpp_entrysearch = Entry(page3)
    dpp_button_6 = Button(page3,text="Search Text",command= lambda:findtext(dpp_entrysearch.get()))
    dpp_button_1.grid_remove()
    dpp_button_2.grid_remove()
    dpp_button_4.grid_remove()
    dpp_button_5.grid(row=2,sticky=W,padx=800)
    dpp_entrysearch.grid(row=2,sticky=W,padx=500,ipady=5,ipadx=20)
    dpp_button_6.grid(row=2,sticky=W,padx=670,ipady=5)

    if(stats == 1):
        stpwrds_extension = []
        dpp_entry_3.delete("1.0", tk.END)
        with open('additional_stop_words_mallet.asw', 'r') as filehandle:
            xy = filehandle.read()
            stpwrds_extension = (xy)
        stpwrds_extension = stpwrds_extension.split('\n')
        stpwrds_extension.sort()
        for x in stpwrds_extension:
            dpp_entry_3.insert(END,x+'\n')
    elif(stats==3):
        stpwrds_extension = []
        dpp_entry_3.delete("1.0", tk.END)
        with open('additional_stop_words_tagalog.asw', 'r') as filehandle:
            xy = filehandle.read()
            stpwrds_extension = (xy)
        stpwrds_extension = stpwrds_extension.split('\n')
        stpwrds_extension.sort()
        for x in stpwrds_extension:
            dpp_entry_3.insert(END,x+'\n')
    else:
        stpwrds_extension = []
        dpp_entry_3.delete("1.0", tk.END)
        with open('additional_stop_words.asw', 'r') as filehandle:
            xy = filehandle.read()
            stpwrds_extension = (xy)
        stpwrds_extension = stpwrds_extension.split('\n')
        stpwrds_extension.sort()
        for x in stpwrds_extension:
            dpp_entry_3.insert(END,x+'\n')
############################################################################
#
#Add New label
def addnewlabel():
    def addnwlbl(lblname,lblmdl,lblhtwrds):
        window_label4 = Label(window,text="Label Added")
        if(lblmdl==1):
            print(1)
            with open("files/ldalabel-"+lblname+".lbl","w") as filehandle:
                filehandle.write(lblhtwrds)
            with open("files/lbllistlda.lst","a") as filehandle:
                filehandle.write(","+lblname)
        elif(lblmdl==2):
            with open("files/malldalabel-"+lblname+".lbl","w") as filehandle:
                filehandle.write(lblhtwrds)
            with open("files/lbllistldamal.lst","a") as filehandle:
                filehandle.write(","+lblname)
        else:
            with open("files/nmflabel-"+lblname+".lbl","w") as filehandle:
                filehandle.write(lblhtwrds)
            with open("files/lbllistnmf.lst","a") as filehandle:
                filehandle.write(","+lblname)
        window_label4.grid(row=5,sticky=W,padx=190)
        window_entry.delete("1.0", tk.END)
        window_texta.delete("1.0", tk.END)
        
    window = tk.Toplevel(main)
    window.title('Add New Label')
    window.minsize(500,320)
    window.maxsize(500,320)

    window_label = Label(window,text="Label Name:",font= "Times 14")
    window_entry = Entry(window)
    window_label2  = Label(window,text="Model:",font= "Times 14")
    window_rbbutvar = IntVar()
    window_rbbut1 = Radiobutton(window,text="Gensim LDA",font= "Times 14", variable=window_rbbutvar, value=1)
    window_rbbut2 = Radiobutton(window,text="Mallet LDA",font= "Times 14", variable=window_rbbutvar, value=2)
    window_rbbut3 = Radiobutton(window,text="NMF",font= "Times 14", variable=window_rbbutvar, value=3)
    window_rbbut1.select()
    window_label3 = Label(window,text="Hitwords:",font= "Times 14",)
    window_texta = Text(window,height=10,width=60)
    window_button = Button(window,text="Add new label",command=lambda:addnwlbl(window_entry.get(),window_rbbutvar.get(),window_texta.get("1.0",END)))

    window_label.grid(row=0,sticky=W,padx=10)
    window_entry.grid(row=0,sticky=W,padx=120)
    window_label2.grid(row=1,sticky=W,padx=10)
    window_rbbut1.grid(row=1,sticky=W,padx=70)
    window_rbbut2.grid(row=1,sticky=W,padx=200)
    window_rbbut3.grid(row=1,sticky=W,padx=320)
    window_label3.grid(row=2,sticky=W,padx=10)
    window_texta.grid(row=3,sticky=W,padx=10)
    window_button.grid(row=4,sticky=W,padx=190,pady=5)
    

############################################################################
#
#Edit labeling
def viewalllabels():
    def switchlabels(*args):
        lebellist = window_opmenu_var.get()
        if(lebellist == 'Gensim LDA'):
            window_opmenu3.grid_remove()
            window_opmenu4.grid_remove()
            window_opmenu2.grid(row=1,sticky=W,padx=200)
        elif(lebellist == 'Mallet LDA'):
            window_opmenu3.grid(row=1,sticky=W,padx=200)
            window_opmenu4.grid_remove()
            window_opmenu2.grid_remove()
        else:
            window_opmenu3.grid_remove()
            window_opmenu4.grid(row=1,sticky=W,padx=200)
            window_opmenu2.grid_remove()
    def chnglbllda(*args):
        window_texta.delete('1.0',END)
        lblname = window_opmenu2_var.get()
        lblname = lblname.replace(' - LDA','')
        flname = 'ldalabel'+'-'+lblname+'.lbl'
        with open('files/'+flname,'r') as flhandle:
            labelwords = flhandle.read()
        window_texta.insert(END,labelwords)
    def chnglbllda2(*args):
        window_texta.delete('1.0',END)
        lblname = window_opmenu3_var.get()
        lblname = lblname.replace(' - LDA(Mallet)','')
        flname = 'malldalabel'+'-'+lblname+'.lbl'
        with open('files/'+flname,'r') as flhandle:
            labelwords = flhandle.read()
        window_texta.insert(END,labelwords)
    def chnglbllda3(*args):
        window_texta.delete('1.0',END)
        lblname = window_opmenu4_var.get()
        lblname = lblname.replace(' - NMF','')
        flname = 'nmflabel'+'-'+lblname+'.lbl'
        with open('files/'+flname,'r') as flhandle:
            labelwords = flhandle.read()
        window_texta.insert(END,labelwords)
        
    window = tk.Toplevel(main)
    window.title('List of All Labels')
    window.minsize(500,320)
    window.maxsize(500,320)

    window_label = Label(window,text="Edit label hitwords")
    window_label2 = Label(window,text="Model:")
    window_label3 = Label(window,text="Labels:")

    listahan = ['Gensim LDA','Mallet LDA','NMF']
    window_opmenu_var = StringVar()
    window_opmenu = OptionMenu(window, window_opmenu_var, *listahan)
    window_opmenu_var.trace("w",switchlabels)
    
    window_opmenu2_var = StringVar(window)
    ldalabels = []
    with open('files/lbllistlda.lst','r') as fileh:
        lbllistlda = fileh.read()
    lbllistlda = lbllistlda.split(',')
    for x in lbllistlda:
        ldalabels.append(x)
    window_opmenu2 = OptionMenu(window, window_opmenu2_var, *ldalabels)
    window_opmenu2_var.trace("w",chnglbllda)
    
    window_opmenu3_var = StringVar(window)
    malldalabels = []
    with open('files/lbllistldamal.lst','r') as fileh:
        lbllistldamal = fileh.read()
    lbllistldamal = lbllistldamal.split(',')
    for x in lbllistldamal:
        malldalabels.append(x)
    window_opmenu3 = OptionMenu(window, window_opmenu3_var, *malldalabels)
    window_opmenu3_var.trace("w",chnglbllda2)
    
    window_opmenu4_var = StringVar(window)
    nmflabels = []
    with open('files/lbllistnmf.lst','r') as fileh:
        lbllistnmf = fileh.read()
    lbllistnmf = lbllistnmf.split(',')
    for x in lbllistnmf:
        nmflabels.append(x+' - NMF')
    window_opmenu4 = OptionMenu(window, window_opmenu4_var, *nmflabels)
    window_opmenu4_var.trace("w",chnglbllda3)

    window_label4 = Label(window,text="Hitwords:")
    window_texta = Text(window,height=10,width=60)
    window_button = Button(window,text="Update label hitwords")

    window_label.grid(row=0,sticky=W,padx=193)
    window_label2.grid(row=1,sticky=W,padx=5)
    window_opmenu.grid(row=1,sticky=W,padx=45)
    window_label3.grid(row=1,sticky=W,padx=160)
    window_opmenu2.grid(row=1,sticky=W,padx=200)

    window_label4.grid(row=2,sticky=W,padx=5)
    window_texta.grid(row=3,sticky=W,padx=8)
    window_button.grid(row=4,sticky=W,padx=190,pady=5)
############################################################################
#
#Remove label
def remlabel():
    def viewlbls(*args):
        window_texta.delete('1.0',END)
        lstname = window_opmenu_var.get()
        if(lstname=='Gensim LDA'):
            with open('files/lbllistlda.lst','r') as file:
                lsta = file.read()
            window_texta.insert(END,lsta)
        elif(lstname=='Mallet LDA'):
            with open('files/lbllistldamal.lst','r') as file:
                lsta = file.read()
            window_texta.insert(END,lsta)
        else:
            with open('files/lbllistnmf.lst','r') as file:
                lsta = file.read()
            window_texta.insert(END,lsta)
    def updtlst():
        vals = window_texta.get('1.0',END)
        lstname = window_opmenu_var.get()
        if(lstname=='Gensim LDA'):
            with open('files/lbllistlda.lst','w') as file:
                file.write(vals)
            window_texta.delete('1.0',END)
        elif(lstname=='Mallet LDA'):
            with open('files/lbllistldamal.lst','w') as file:
                file.write(vals)
            window_texta.delete('1.0',END)
        else:
            with open('files/lbllistnmf.lst','w') as file:
                file.write(vals)
            window_texta.delete('1.0',END)

    window = tk.Toplevel(main)
    window.title('Remove a label')
    window.minsize(500,320)
    window.maxsize(500,320)

    window_label = Label(window,text="Model")
    listahan = ['Gensim LDA','Mallet LDA','NMF']
    window_opmenu_var = StringVar()
    window_opmenu = OptionMenu(window, window_opmenu_var, *listahan)
    window_opmenu_var.set('-------')
    window_opmenu_var.trace("w",viewlbls)
    window_label2 = Label(window,text="Labels")
    window_texta = Text(window,height=10,width=60)
    window_button = Button(window,text="Update List",command=lambda:updtlst())
    
    window_label.grid(row=0,sticky=W,padx=5)
    window_opmenu.grid(row=1,sticky=W,padx=45)
    window_label2.grid(row=2,sticky=W,padx=5)
    window_texta.grid(row=3,sticky=W,padx=8)
    window_button.grid(row=4,sticky=W,padx=190,pady=5)
############################################################################
#
#Import another csv file
def importdataset():
    def openimport(name):
        os.system("start EXCEL.EXE "+name)
    def importdtast(impfile,colname,expfile):
        expfile = expfile + '.csv'
        window_label6 = Label(window,text="Data Imported saved as "+expfile)
        window_button2 = Button(window,text="Open in Excel",command=lambda:openimport(expfile))
        
        data = pd.read_csv(impfile, error_bad_lines=False)
        # We only need the Headlines text column from the data
        data_text = data[[colname]]
        data[['data']] = data[[colname]]
        data_text = data[['data']]
        data_text = data_text.astype('str');
        data = data_text.data.values.tolist()
        with open(expfile,'w') as filehandle:
            filehandle.write('data\n')
            for x in data:
                filehandle.write(str((x).encode("utf-8"))+"\n")
        window_label6.grid(row=5,sticky=W)
        window_button2.grid(row=5,sticky=W,padx=210)
    
    window = tk.Toplevel(main)
    window.title('Import another dataset')
    window.minsize(350,140)
    window.maxsize(350,140)

    window_label = Label(window,text="Import a csv file")
    window_label2 = Label(window,text="Filename of csv file to be imported")
    window_label3 = Label(window,text="Column name of the data to be imported")
    window_label4 = Label(window,text="Filename of the imported csv file")
    window_label5 = Label(window,text=".csv")
    
    window_entry = Entry(window)
    window_entry2 = Entry(window)
    window_entry3 = Entry(window)
    window_entry3.insert(END,'importeddataset')

    window_button = Button(window,text="Import file",command=lambda:importdtast(window_entry.get(),window_entry2.get(),window_entry3.get()))

    window_label.grid(row=0,sticky=W,padx=120)
    window_label2.grid(row=1,sticky=W)
    window_label3.grid(row=2,sticky=W)
    window_label4.grid(row=3,sticky=W)
    window_label5.grid(row=3,sticky=W,padx=300)
    window_entry.grid(row=1,sticky=W,padx=190)
    window_entry2.grid(row=2,sticky=W,padx=230)
    window_entry3.grid(row=3,sticky=W,padx=180)
    window_button.grid(row=4,sticky=W,padx=120)
############################################################################
#
#Switch Menu
def switchmenu(algo):
    if(algo=="NMF"):
        ldaparam_label_1.grid_remove()
        ldaparam_entry_1.grid_remove()
        ldaparam_label_6.grid_remove()
        ldaparam_entry_6.grid_remove()
        ldaparam_label_3.grid_remove()
        ldaparam_entry_3.grid_remove()
        ldaparam_label_5.grid_remove()
        ldaparam_entry_5.grid_remove()
        ldaparam_label_7.grid_remove()
        ldaparam_opmenu.grid_remove()

        nmfparam_label_1.grid(row=3,sticky=W)
        nmfparam_entry_1.grid(row=3,sticky=W,padx=115)
        nmfparam_label_3.grid(row=3,sticky=W,padx=185)
        nmfparam_entry_3.grid(row=3,sticky=W,padx=330)
        nmfparam_label_2.grid(row=4,sticky=W)
        nmfparam_entry_2.grid(row=4,sticky=W,padx=220)
        nmfparam_label_4.grid(row=5,sticky=W)
        nmfparam_entry_4.grid(row=5,sticky=W,padx=90)
    else:
        nmfparam_label_1.grid_remove()
        nmfparam_entry_1.grid_remove()
        nmfparam_label_3.grid_remove()
        nmfparam_entry_3.grid_remove()
        nmfparam_label_2.grid_remove()
        nmfparam_entry_2.grid_remove()
        nmfparam_label_4.grid_remove()
        nmfparam_entry_4.grid_remove()
        
        ldaparam_label_1.grid(row=3,sticky=W)
        ldaparam_entry_1.grid(row=3,sticky=W,padx=115)
        ldaparam_label_6.grid(row=3,sticky=W,padx=185)
        ldaparam_entry_6.grid(row=3,sticky=W,padx=330)
        ldaparam_label_3.grid(row=4,sticky=W)
        ldaparam_entry_3.grid(row=4,sticky=W,padx=90)
        ldaparam_label_5.grid(row=5,sticky=W)
        ldaparam_entry_5.grid(row=5,sticky=W,padx=140)
        ldaparam_label_7.grid(row=7,sticky=W)
        ldaparam_opmenu.grid(row=7,sticky=W,padx=120)

main.mainloop()
