from submodules import topicmodel as t2
from submodules import usrmodules as usmdls
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
collect_label_32 = Label(page1, text = "Date",pady=20, font= "Times 15")
collect_label_3 = Label(page1, text = "From:", font= "Times 15")
collect_label_4 = Label(page1, text = "To:", pady=20, font= "Times 15")
collect_button = Button(page1, text ="Collect Data", font ="Times 15", borderwidth=3, relief ="solid", command=lambda: dataclct(collect_entry_1.get(), collect_entry_2.get(), collect_entry_3.get(), collect_entry_4.get(),))


collect_entry_1 = Entry(page1)
collect_entry_2 = Entry(page1)
collect_entry_2.insert(END, '100')
collect_entry_3 = Entry(page1)
collect_entry_3.insert(END, '2018-01-01')
collect_entry_4 = Entry(page1)
collect_entry_4.insert(END, '2019-01-01')

collect_label_1.grid(row=0, sticky=W)
collect_label_2.grid(row=1)
collect_label_32.grid(row=2, sticky=W)
collect_label_3.grid(row=3, sticky=W)
collect_label_4.grid(row=4, sticky=W)
collect_button.grid(row=5, sticky=E)

collect_entry_1.grid(row=0, column=1)
collect_entry_2.grid(row=1, column=1)
collect_entry_3.grid(row=3, column=1)
collect_entry_4.grid(row=4, column=1)



page2 =  ttk.Frame(nb)
nb.add(page2, text ='Generate Topic Models')
tpcmdl_label_1 = Label(page2, text ="Generate topics using LDA and NMF", pady=20,font= "Times 15")
tpcmdl_label_2 = Label(page2, text = "Enter no. of topics:",pady=30, font= "Times 15")
tpcmdl_button = Button(page2, text ="Browse", font ="Times 15", borderwidth=3, relief="solid")
tpcmdl_button1 = Button(page2, text ="Generate Topic Keywords", font ="Times 15", borderwidth=3, relief="solid", command=lambda: genertp(tpcmdl_entry_1.get()))
tpcmdl_label_3 = Label(page2, text = "Filename:",pady=30, font= "Times 15")

tpcmdl_label_1.grid(row=0, sticky=W)
#tpcmdl_button.grid(row=1, sticky=E)
tpcmdl_label_3.grid(row=1, sticky=W)
tpcmdl_label_2.grid(row=2, sticky=W)
tpcmdl_button1.grid(row=3, sticky=E)


tpcmdl_entry_1 = Entry(page2, width ="35")
tpcmdl_entry_2 = Entry(page2, width ="20")


tpcmdl_entry_1.grid(row=1, column=0, sticky = E)
tpcmdl_entry_2.grid(row=2, column=0, sticky = E)
num = int(20)
tpcmdl_entry_2.insert(END, num)


def genertp(name):
    def donothing():
        print("Do nothing")
    def topicmdling(name):
        window1status_label.config(text = 'Cleaning') 
        cleaned = t2.cleaning(name)
        window1status_label.config(text = 'Creating Corpus')
        corpus = t2.mkcorpus(cleaned)
        window1status_label.config(text = 'Training')
        t2.mallda(corpus,cleaned)
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
    viewresults_button = Button(window1, text ="View Results", font ="Times 11", borderwidth=3, command=lambda: donothing)
    tpcbar_progressbar = Progressbar(window1, orient=HORIZONTAL,length=100,  mode='indeterminate')
    
    window1status_label.pack()
    tpcbar_progressbar.pack()
    tpcbar_progressbar.start()
    window1.Queue = Queue.Queue()
    ThreadedTask(window1.Queue).start()
    window1.main.after(100,window1.process_queue)
    
def dataclct(query,num,startd,endd):
    def donothing():
        print("Do nothing")
    def collection(query,num,startd,endd):
        window2status_label.config(text = 'Cleaning') 
        usmdls.collectdata(query,num,startd,endd)
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
            viewresults2_button.pack()
            self.queue.put("Task finished")
            
    window2 = tk.Toplevel(main)
    window2.title('Generating...')
    window2.minsize(280,100)
    window2.maxsize(280,100)
    window2status_label = Label(window2, text = "Processing",pady=10, font= "Times 11")
    viewresults2_button = Button(window2, text ="View Results", font ="Times 11", borderwidth=3, command=lambda: donothing)
    clctbar_progressbar = Progressbar(window2, orient=HORIZONTAL,length=100,  mode='indeterminate')
    
    window2status_label.pack()
    clctbar_progressbar.pack()
    clctbar_progressbar.start()
    window2.Queue = Queue.Queue()
    ThreadedTask(window2.Queue).start()
    window1.main.after(100,window2.process_queue)
       
main.mainloop()
