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


main = Tk()
main.title('Topic Analysis on Mayon Volcano Tweet')
main.geometry('500x500')
main.maxsize(500,500)
main.minsize(500,500)

rows = 0
while rows<50:
    main.rowconfigure(rows, weight=1)
    main.columnconfigure(rows, weight =1)
    rows +=1

nb = ttk.Notebook(main)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')


page1 = ttk.Frame(nb)
nb.add(page1, text='Collect Data')

collect_label_1 = Label(page1, text ="Enter keyword:", pady=20,font= "Times 15")
collect_label_2 = Label(page1, text = "Enter max no. of tweets:", font= "Times 15")
collect_label_21 = Label(page1, text = "yyyy-mm-dd",font= "Times 10")
collect_label_32 = Label(page1, text = "Date",font= "Times 15")
collect_label_3 = Label(page1, text = "From:", font= "Times 15")
collect_label_4 = Label(page1, text = "To:", pady=20, font= "Times 15")
collect_label_5 = Label(page1, text = "Filename:",pady=20, font="Times 15")
collect_button = Button(page1, text ="Collect Data", font ="Times 15", borderwidth=3, relief ="solid", command=lambda: dataclct(collect_entry_1.get(), collect_entry_2.get(), collect_entry_3.get(), collect_entry_4.get(),))


collect_entry_1 = Entry(page1)
collect_entry_2 = Entry(page1)
collect_entry_2.insert(END, '100')
collect_entry_3 = Entry(page1)
collect_entry_3.insert(END, '2018-01-01')
collect_entry_4 = Entry(page1)
collect_entry_4.insert(END, '2019-01-01')
collect_entry_5 = Entry(page1, width="35")

collect_label_1.grid(row=0, sticky=W)
collect_label_2.grid(row=1)
collect_label_21.grid(row=3, column=1)
collect_label_32.grid(row=3, sticky=W)
collect_label_3.grid(row=4, sticky=W)
collect_label_4.grid(row=5, sticky=W)
collect_label_5.grid(row=6, sticky=W)
collect_button.grid(row=7, column=1)

collect_entry_1.grid(row=0, column=1)
collect_entry_2.grid(row=1, column=1)
collect_entry_3.grid(row=4, column=1)
collect_entry_4.grid(row=5, column=1)
collect_entry_5.grid(row=6, column=1)
now = datetime.datetime.now()
collect_entry_5.insert(END,'collecteddata-'+str(now.strftime("%Y-%m-%d")))

collect_entry_1_ttp = ttp.CreateToolTip(collect_entry_1, "Query keyword found in tweets")
collect_entry_2_ttp = ttp.CreateToolTip(collect_entry_2, "Max number of tweets to be gathered")
collect_entry_3_ttp = ttp.CreateToolTip(collect_entry_3, "Start date of collecting")
collect_entry_4_ttp = ttp.CreateToolTip(collect_entry_4, "End date of collecting")
collect_entry_5_ttp = ttp.CreateToolTip(collect_entry_5, "filename of the csv file")


page3 =  ttk.Frame(nb)
nb.add(page3, text ='Data Pre-proccessing')
dpp_label_1 = Label(page3, text="Data Pre-processing:", font = "Times 15", pady=10)
dpp_label_2 = Label(page3, text="CSV Filename:", font = "Times 15", pady=20)
dpp_label_3 = Label(page3, text="Remove:", font = "Times 15")
dpp_label_4 = Label(page3, text="Bigrams and Trigrams", font = "Times 15",pady=10)
dpp_label_5 = Label(page3, text="Min. Count:", font = "Times 14")
dpp_label_6 = Label(page3, text="Bigram Threshold:", font = "Times 14")
dpp_label_7 = Label(page3, text="Trigram Threshold:", font = "Times 14")

emailvar = IntVar()
dpp_checkbox_1 = Checkbutton(page3, text = "Emails", font = "Times 15", variable=emailvar)
dpp_checkbox_1.select()
speccharvar = IntVar()
dpp_checkbox_2 = Checkbutton(page3, text = "Special characters(ex:@#!$%^)", font = "Times 15", variable=speccharvar)
dpp_checkbox_2.select()
linkvar = IntVar()
dpp_checkbox_3 = Checkbutton(page3, text = "Links", font = "Times 15", variable=linkvar)
dpp_checkbox_3.select()
stpwrdvar = IntVar()
dpp_checkbox_4 = Checkbutton(page3, text = "Remove Stopwords", font = "Times 14", variable=stpwrdvar)
dpp_checkbox_4.select()

dpp_entry_1 = Entry(page3, width ="35")
dpp_entry_2 = Entry(page3)
dpp_entry_2.insert(END, '5')
dpp_entry_3 = Entry(page3)
dpp_entry_3.insert(END, '100')
dpp_entry_4 = Entry(page3)
dpp_entry_4.insert(END, '100')

dpp_button_1 = Button(page3, text ="General Stopwords", font ="Times 15", borderwidth=3, relief ="solid", command=lambda: viewstopwrds(main,1))
dpp_button_2 = Button(page3, text ="Additional Stopwords", font ="Times 15", borderwidth=3, relief ="solid", command=lambda: viewstopwrds(main,2))
dpp_button_3 = Button(page3, text ="Clean Data  File", font ="Times 15", borderwidth=3, relief ="solid", padx=30, command=lambda: datacleaning(main,dpp_entry_1.get()))

dpp_label_1.grid(row=0, sticky=W)
dpp_label_2.grid(row=1, sticky=W)
dpp_label_3.grid(row=2, sticky=W)
dpp_label_4.grid(row=5, sticky=W)
dpp_label_5.grid(row=6, sticky=W)
dpp_label_6.grid(row=7, sticky=W)
dpp_label_7.grid(row=8, sticky=W)
dpp_checkbox_1.grid(row=3,column=0)
dpp_checkbox_2.grid(row=3,column=1)
dpp_checkbox_3.grid(row=4,column=0)
dpp_checkbox_4.grid(row=9,column=0)

dpp_checkbox_1_ttp = ttp.CreateToolTip(dpp_checkbox_1, "@")
dpp_checkbox_2_ttp = ttp.CreateToolTip(dpp_checkbox_2, "https,www,http")
dpp_checkbox_3_ttp = ttp.CreateToolTip(dpp_checkbox_3, "!@#$#%")
dpp_checkbox_4_ttp = ttp.CreateToolTip(dpp_checkbox_4, "Remove all stopwords")


dpp_entry_1.grid(row=1, column=1)
dpp_entry_2.grid(row=6, column=1)
dpp_entry_3.grid(row=7, column=1)
dpp_entry_4.grid(row=8, column=1)

dpp_entry_1_ttp = ttp.CreateToolTip(dpp_entry_1, "Filename of the csv file to be  cleaned")
dpp_entry_2_ttp = ttp.CreateToolTip(dpp_entry_2, "Ignore all words and bigrams with total collected count lower than this value.")
dpp_entry_3_ttp = ttp.CreateToolTip(dpp_entry_3, "Bigram score threshold for forming the phrases (higher means fewer phrases). A phrase of words a followed by b is accepted if the score of the phrase is greater than threshold. Heavily depends on concrete scoring-function, see the scoring parameter.")
dpp_entry_4_ttp = ttp.CreateToolTip(dpp_entry_4, "Trigram score threshold for forming the phrases (higher means fewer phrases). A phrase of words a followed by b is accepted if the score of the phrase is greater than threshold. Heavily depends on concrete scoring-function, see the scoring parameter.")
dpp_button_1.grid(row=10, column=0)
dpp_button_2.grid(row=10, column=1)
dpp_button_3.grid(pady =5 ,row=12,columnspan=3)

page2 =  ttk.Frame(nb)
nb.add(page2, text ='Generate Topic Models')
tpcmdl_label_1 = Label(page2, text ="Generate topics using LDA and NMF", font= "Times 15")
tpcmdl_label_2 = Label(page2, text = "Enter no. of topics:",pady=30, font= "Times 15")
tpcmdl_button = Button(page2, text ="Browse", font ="Times 15", borderwidth=3, relief="solid")
tpcmdl_button1 = Button(page2, text ="Generate Topic Keywords", font ="Times 15", borderwidth=3, relief="solid", command=lambda: genertp(tpcmdl_entry_1.get()))
tpcmdl_label_3 = Label(page2, text = "Filename:",pady=10, font= "Times 15")
tpcmdl_entry_1 = Entry(page2, width ="35")
tpcmdl_entry_1.insert(END,'cleaneddata.cds')
tpcmdl_entry_2 = Entry(page2, width ="20")

tpcmdl_label_4 = Label(page2, text = "LDA Parameters",pady=10, font= "Times 15")
ldaparam_label_1 = Label(page2, text = "Num. Topics:",pady=3, font= "Times 12")
ldaparam_entry_1 = Entry(page2, width ="15")
ldaparam_entry_1.insert(END,int(20))
ldaparam_label_2 = Label(page2, text = "Random State:",pady=3, font= "Times 12")
ldaparam_entry_2 = Entry(page2, width ="15")
ldaparam_entry_2.insert(END,int(100))
ldaparam_label_3 = Label(page2, text = "Update Every",pady=3, font= "Times 12")
ldaparam_entry_3 = Entry(page2, width ="15")
ldaparam_entry_3.insert(END,int(1))
ldaparam_label_4 = Label(page2, text = "Chunk Size",pady=3, font= "Times 12")
ldaparam_entry_4 = Entry(page2, width ="15")
ldaparam_entry_4.insert(END,int(100))
ldaparam_label_5 = Label(page2, text = "Training Passes",pady=3, font= "Times 12")
ldaparam_entry_5 = Entry(page2, width ="15")
ldaparam_entry_5.insert(END,int(10))
ldaparam_label_6 = Label(page2, text = "Word Per Topic",pady=3, font= "Times 12")
ldaparam_entry_6 = Entry(page2, width ="15")
ldaparam_entry_6.insert(END,int(10))
tpcmdl_label_5 = Label(page2, text = "NMF Parameters",pady=10, font= "Times 15")
nmfparam_label_1 = Label(page2, text = "Num. Topics",pady=3, font= "Times 12")
nmfparam_entry_1 = Entry(page2, width ="5")
nmfparam_entry_1.insert(END,int(20))
nmfparam_label_2 = Label(page2, text = "Vectorizer Max Features",pady=3, font= "Times 12")
nmfparam_entry_2 = Entry(page2, width ="5")
nmfparam_entry_2.insert(END,int(5000))
nmfparam_label_3 = Label(page2, text = "Vectorizer Min DF",pady=3, font= "Times 12")
nmfparam_entry_3 = Entry(page2, width ="5")
nmfparam_entry_3.insert(END,int(1))
nmfparam_label_4 = Label(page2, text = "Vectorizer Max DF",pady=3, font= "Times 12")
nmfparam_entry_4 = Entry(page2, width ="5")
nmfparam_entry_4.insert(END,float(1.0))

tpcmdl_entry_1_ttp = ttp.CreateToolTip(tpcmdl_entry_1, "File name of the cleaned data set")
ldaparam_entry_1_ttp = ttp.CreateToolTip(ldaparam_entry_1, "The number of requested latent topics to be extracted from the training corpus.")
ldaparam_entry_2_ttp = ttp.CreateToolTip(ldaparam_entry_2, "Random state is the seed used by the random number generator")
ldaparam_entry_3_ttp = ttp.CreateToolTip(ldaparam_entry_3, "Number of documents to be iterated through for each update. Set to 0 for batch learning, > 1 for online iterative learning")
ldaparam_entry_4_ttp = ttp.CreateToolTip(ldaparam_entry_4, "Number of documents to be used in each training chunk.")
ldaparam_entry_5_ttp = ttp.CreateToolTip(ldaparam_entry_5, "Number of passes through the corpus during training")
ldaparam_entry_6_ttp = ttp.CreateToolTip(ldaparam_entry_6, "Number of words to be generated per topic")
nmfparam_entry_1_ttp = ttp.CreateToolTip(nmfparam_entry_1, "Number of topics to be generated by the model")
nmfparam_entry_2_ttp = ttp.CreateToolTip(nmfparam_entry_2, "Builds a vocabulary that only consider the top max_features ordered by term frequency across the corpus")
nmfparam_entry_3_ttp = ttp.CreateToolTip(nmfparam_entry_3, "When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words). Minimum value")
nmfparam_entry_4_ttp = ttp.CreateToolTip(nmfparam_entry_4, "When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words). Maximum value must be in float and higher than min value")






tpcmdl_label_1.grid(row=0, sticky=W)
#tpcmdl_button.grid(row=1, sticky=E)
tpcmdl_label_3.grid(row=1, sticky=W)
tpcmdl_entry_1.grid(row=1, column=0, sticky = E)

tpcmdl_label_4.grid(row=2, sticky=W)
ldaparam_label_1.grid(row=3,sticky=W)
ldaparam_entry_1.grid(row=3)
ldaparam_label_2.grid(row=4,sticky=W)
ldaparam_entry_2.grid(row=4)
ldaparam_label_3.grid(row=5,sticky=W)
ldaparam_entry_3.grid(row=5)
ldaparam_label_4.grid(row=6,sticky=W)
ldaparam_entry_4.grid(row=6)
ldaparam_label_5.grid(row=7,sticky=W)
ldaparam_entry_5.grid(row=7)
ldaparam_label_6.grid(row=8,sticky=W)
ldaparam_entry_6.grid(row=8)
tpcmdl_label_5.grid(row=2, column=1,sticky=E)
nmfparam_label_1.grid(row=3,column=1)
nmfparam_entry_1.grid(row=3,column=2,sticky=E)
nmfparam_label_2.grid(row=4,column=1)
nmfparam_entry_2.grid(row=4,column=2,sticky=E)
nmfparam_label_3.grid(row=5,column=1)
nmfparam_entry_3.grid(row=5,column=2,sticky=E)
nmfparam_label_4.grid(row=6,column=1)
nmfparam_entry_4.grid(row=6,column=2,sticky=E)

tpcmdl_button1.grid(row=9,columnspan=3,pady=50)

def genertp(name):
    def viewresults(window):
        print('ok')
        window.destroy()
        new=2
        webbrowser.open('viewresults.html',new=new)
    def topicmdling(name):
        with open(name, 'rb') as filehandle:
            cleaned = pickle.load(filehandle) 
        print(cleaned)
        window1status_label.config(text = 'Creating Corpus')
        corpus = t2.mkcorpus(cleaned)
        window1status_label.config(text = 'LDA Training')
        print(int(ldaparam_entry_1.get()))
        outres1 = t2.ldamdl(corpus,cleaned,int(ldaparam_entry_1.get()) ,int(ldaparam_entry_2.get()) ,int(ldaparam_entry_3.get()) ,int(ldaparam_entry_4.get()) ,int(ldaparam_entry_5.get()) ,int(ldaparam_entry_6.get()))
        fl1 = open("ldaresult.res","w")
        fl1.write("".join(outres1))
        fl1.close()
        window1status_label.config(text = 'NMF Training')
        outres2 =t2.nmfmdl(cleaned,int(nmfparam_entry_1.get()) ,int(nmfparam_entry_2.get()),int(nmfparam_entry_3.get()) ,float(nmfparam_entry_4.get()))
        fl2 = open("nmfresult.res","w")
        fl2.writelines("".join(outres2))
        fl2.close()
        genresults()    
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
            topicmdling(name)  # Simulate long running process
            tpcbar_progressbar.stop()
            tpcbar_progressbar.destroy()
            window1status_label.config(text = 'Completed')
            viewresults_button.pack()
            self.queue.put("Task finished")
    
    window1 = tk.Toplevel(main)
    window1.title('Generating...')
    window1.minsize(280,100)
    window1.maxsize(280,100)
    window1status_label = Label(window1, text = "Processing",pady=10, font= "Times 11")
    viewresults_button = Button(window1, text ="View Results", font ="Times 11", borderwidth=3, command=lambda: viewresults(window1))
    tpcbar_progressbar = Progressbar(window1, orient=HORIZONTAL,length=100,  mode='indeterminate')
    
    window1status_label.pack()
    tpcbar_progressbar.pack()
    tpcbar_progressbar.start()
    window1.Queue = Queue.Queue()
    ThreadedTask(window1.Queue).start()
    window1.main.after(100,window1.process_queue)
    
def dataclct(query,num,startd,endd):
    def opendir(window):
        dir_path = os.path.dirname(os.path.realpath(__file__))# open current directory
        subprocess.check_call(['explorer', dir_path])
        window.destroy()
    def openfl():
        os.system("start EXCEL.EXE output_got.csv")
    def collection(query,num,startd,endd):
        window2status_label.config(text = 'Collecting...') 
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
            collection(query,num,startd,endd)  # Simulate long running process
            clctbar_progressbar.stop()
            clctbar_progressbar.destroy()
            window2status_label.config(text = 'Completed')
            openfile_button.pack()
            viewresults2_button.pack()
            self.queue.put("Task finished")
            
    window2 = tk.Toplevel(main)
    window2.title('Collection Status')
    window2.minsize(280,100)
    window2.maxsize(280,100)
    window2status_label = Label(window2, text = "Processing",pady=10, font= "Times 11")
    viewresults2_button = Button(window2, text ="Open in Explorer", font ="Times 11", borderwidth=3, command=lambda: opendir(window2))
    openfile_button = Button(window2, text ="Open File", font ="Times 11", borderwidth=3, command=lambda: openfl())
    clctbar_progressbar = Progressbar(window2, orient=HORIZONTAL,length=100,  mode='indeterminate')
    
    window2status_label.pack()
    clctbar_progressbar.pack()
    clctbar_progressbar.start()
    window2.Queue = Queue.Queue()
    ThreadedTask(window2.Queue).start()
    window1.main.after(100,window2.process_queue)

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
def datacleaning(main,name):
    def cleaningdata(name):
        window1status_label.config(text = 'Cleaning')
        cleaned = t2.cleaning(name,emailvar.get(),linkvar.get(),speccharvar.get(),dpp_entry_2.get(),dpp_entry_3.get(),dpp_entry_4.get(),stpwrdvar.get())
        print(cleaned)
        with open("cleaneddata.cds","wb") as filehandle:
            pickle.dump(cleaned,filehandle)
         #   for listitem in cleaned:
          #      filehandle.write('%s\n' % listitem)
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
            cleaningdata(name)  # Simulate long running process
            tpcbar_progressbar.stop()
            tpcbar_progressbar.destroy()
            window1status_label.config(text = 'Completed')
            viewresults_button.pack()
            self.queue.put("Task finished")

    window1 = tk.Toplevel(main)
    window1.title('Pre-processing')
    window1.minsize(280,100)
    window1.maxsize(280,100)
    window1status_label = Label(window1, text = "Processing",pady=10, font= "Times 11")
    viewresults_button = Button(window1, text ="Close", font ="Times 11", borderwidth=3, command=lambda: window1.destroy())
    tpcbar_progressbar = Progressbar(window1, orient=HORIZONTAL,length=100,  mode='indeterminate')

    window1status_label.pack()
    tpcbar_progressbar.pack()
    tpcbar_progressbar.start()
    window1.Queue = Queue.Queue()
    ThreadedTask(window1.Queue).start()
    window1.main.after(100,window1.process_queue)

def viewstopwrds(main,stats):
    window = tk.Toplevel(main)
    if(stats == 1):
        window.title('General Stopwords')
        window.minsize(450,450)
        window.maxsize(450,450)
        gtspwrds_label_1 = Label(window, text = "Stopwords List",pady=10, font= "Times 15")
        gtspwrds_entry_1 = Text(window, width=50, height=22,wrap='word')
        scrollb = Scrollbar(window)
        gtspwrds_entry_1.configure(yscrollcommand=scrollb.set)
        
        from nltk.corpus import stopwords
        stop_words = stopwords.words('english')
        gtspwrds_entry_1.insert(END,stop_words)
        
        gtspwrds_label_1.pack()
        gtspwrds_entry_1.pack()
    else:
        def updatestpwrds(stpwrds_extension):
            with open("additional_stop_words.asw","wb") as filehandle:
                pickle.dump(stpwrds_extension,filehandle)
            gtspwrds_label_2 = Label(window, text = "Updated Stopwords",pady=10, font= "Times 12")
            gtspwrds_label_2.pack()
        window.title('Additional Stopwords')
        window.minsize(450,450)
        window.maxsize(450,450)

        from nltk.corpus import stopwords
        stop_words = stopwords.words('english')
        with open('additional_stop_words.asw', 'rb') as filehandle:
            stpwrds_extension = pickle.load(filehandle)
        stop_words.extend(stpwrds_extension)
        
        gtspwrds_label_1 = Label(window, text = "Add,Remove,Edit Stopwords",pady=10, font= "Times 15")
        gtspwrds_entry_1 = Text(window, width=50, height=22,wrap='word')
        gtspwrds_button_1 = Button(window, text ="Update", font ="Times 11", borderwidth=3, command=lambda: updatestpwrds(gtspwrds_entry_1.get("1.0",END)))
        scrollb = Scrollbar(window)
        #gtspwrds_entry_1.configure(yscrollcommand=scrollb.set)
        gtspwrds_entry_1.insert(END,stpwrds_extension)

        print(gtspwrds_entry_1.get("1.0",END))
        gtspwrds_label_1.pack()
        gtspwrds_entry_1.pack()
        gtspwrds_button_1.pack()
main.mainloop()
